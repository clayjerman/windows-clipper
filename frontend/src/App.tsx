import { useState, useEffect, useCallback } from 'react';
import MainLayout from './components/Layout/MainLayout';
import { ApiKeySetup } from './components/Onboarding';
import { SettingsPanel } from './components/Settings';
import { hasApiKeys } from './services/settingsStorage';
import { useLog } from './hooks/useLog';
import BackendSplash from './components/BackendSplash';

const BACKEND = 'http://127.0.0.1:58174';
const HEALTH_TIMEOUT_S = 40;

function useBackendReady() {
  const [ready, setReady] = useState(false);
  const [timedOut, setTimedOut] = useState(false);
  const [attempt, setAttempt] = useState(0);

  const start = useCallback(() => {
    setReady(false);
    setTimedOut(false);
    setAttempt((n) => n + 1);
  }, []);

  useEffect(() => {
    if (attempt === 0) {
      setAttempt(1); // kick off on mount
      return;
    }
    let cancelled = false;
    let tries = 0;

    const poll = async () => {
      while (!cancelled) {
        try {
          const res = await fetch(`${BACKEND}/health`, {
            signal: AbortSignal.timeout(1500),
          });
          if (res.ok) {
            if (!cancelled) setReady(true);
            return;
          }
        } catch {
          // backend not up yet
        }
        tries++;
        if (tries >= HEALTH_TIMEOUT_S) {
          if (!cancelled) setTimedOut(true);
          return;
        }
        await new Promise((r) => setTimeout(r, 1000));
      }
    };

    poll();
    return () => { cancelled = true; };
  }, [attempt]);

  return { ready, timedOut, retry: start };
}

function App() {
  const { ready: backendReady, timedOut, retry } = useBackendReady();

  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [isSetupComplete, setIsSetupComplete] = useState(false);

  const [url, setUrl] = useState('');
  const [isUrlValid, setIsUrlValid] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState('');
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  const [clips, setClips] = useState<any[]>([]);
  const [selectedClips, setSelectedClips] = useState<Set<string>>(new Set());

  const { entries: logEntries, unread: logUnread, addLog, clearLog, markRead } = useLog();

  useEffect(() => {
    const hasKeys = hasApiKeys();
    setShowOnboarding(!hasKeys);
    setIsSetupComplete(hasKeys);
  }, []);

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
    setIsSetupComplete(true);
  };

  const handleSettingsClose = () => {
    setShowSettings(false);
    const hasKeys = hasApiKeys();
    if (!hasKeys && isSetupComplete) {
      setShowOnboarding(true);
    }
  };

  const handleGenerate = useCallback(async () => {
    if (!isUrlValid) return;

    setProcessing(true);
    setCurrentStage('Connecting...');
    setProgress(0);
    setMessage('Connecting to backend...');
    setClips([]);
    setSelectedClips(new Set());
    addLog('info', `Starting generation for: ${url}`);

    const stageLabels: Record<string, string> = {
      downloading: 'Downloading video...',
      transcribing: 'Transcribing audio...',
      analyzing: 'Analyzing content...',
      scoring: 'Scoring viral moments...',
      detecting: 'Detecting speakers...',
      editing: 'Generating clips...',
    };

    let ws: WebSocket;

    try {
      ws = new WebSocket(`ws://127.0.0.1:58174/ws`);
    } catch {
      const msg = 'Cannot connect to backend. Make sure the server is running on port 58174.';
      setCurrentStage('Error');
      setMessage(msg);
      setProcessing(false);
      addLog('error', msg);
      return;
    }

    ws.onerror = () => {
      const msg = 'Cannot reach backend at 127.0.0.1:58174. Please start the server first.';
      setCurrentStage('Connection Error');
      setMessage(msg);
      setProcessing(false);
      addLog('error', msg);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.type === 'progress') {
          const data = msg.data;
          const label = stageLabels[data.stage] || data.stage;
          setCurrentStage(label);
          setProgress(data.progress ?? 0);
          setMessage(data.message || '');
          if (data.progress === 0 || data.progress === 100) {
            addLog('info', `[${label}] ${data.message || ''}`);
          }
        } else if (msg.type === 'clip_generated') {
          const clip = msg.data;
          const score = clip.score > 10 ? Math.round(clip.score) : Math.round(clip.score * 10);
          setClips((prev) => [
            ...prev,
            {
              id: clip.id,
              title: clip.title,
              duration: Math.round(clip.duration),
              score,
              thumbnail: `${BACKEND}/api/clips/${clip.id}/thumbnail`,
              videoUrl: `${BACKEND}/api/clips/${clip.id}/video`,
              description: clip.description,
            },
          ]);
          addLog('success', `Clip generated: "${clip.title}" (score: ${score}%)`);
        } else if (msg.type === 'complete') {
          setCurrentStage('Complete!');
          setProgress(100);
          setMessage('Your clips are ready! Click a clip to preview it.');
          setProcessing(false);
          addLog('success', `Generation complete. ${clips.length + 1} clip(s) ready.`);
          ws.close();
        } else if (msg.type === 'error') {
          const errMsg = msg.data?.error || 'Processing failed';
          setCurrentStage('Error');
          setMessage(errMsg);
          setProcessing(false);
          addLog('error', `Generation failed: ${errMsg}`);
          ws.close();
        }
      } catch {
        // ignore parse errors
      }
    };

    ws.onopen = async () => {
      try {
        setCurrentStage('Downloading video...');
        setMessage('Starting download from YouTube...');
        setProgress(5);
        addLog('info', 'WebSocket connected. Sending generate request...');

        const response = await fetch(`${BACKEND}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url,
            settings: {
              clip_duration: 30,
              num_clips: 5,
              subtitle_style: 'default',
              zoom_effect: false,
            },
          }),
        });

        if (!response.ok) {
          const err = await response.json().catch(() => ({}));
          throw new Error(err.detail || 'Failed to start generation');
        }

        const data = await response.json();
        addLog('info', `Job started: ${data.job_id}`);
      } catch (error) {
        const errMsg = error instanceof Error ? error.message : 'Failed to start processing';
        setCurrentStage('Error');
        setMessage(errMsg);
        setProcessing(false);
        addLog('error', `Generate request error: ${errMsg}`);
        ws.close();
      }
    };
  }, [isUrlValid, url, addLog, clips.length]);

  const handleExport = useCallback(async () => {
    if (selectedClips.size === 0) return;

    setProcessing(true);
    setCurrentStage('Exporting...');
    setProgress(0);
    setMessage('Preparing clips for export...');

    const clipIds = Array.from(selectedClips);
    addLog('info', `Exporting ${clipIds.length} clip(s)...`);

    let ws: WebSocket;
    try {
      ws = new WebSocket(`ws://127.0.0.1:58174/ws`);
    } catch {
      const msg = 'Cannot connect to backend.';
      setCurrentStage('Export Error');
      setMessage(msg);
      setProcessing(false);
      addLog('error', msg);
      return;
    }

    ws.onerror = () => {
      const msg = 'Cannot reach backend at 127.0.0.1:58174.';
      setCurrentStage('Export Error');
      setMessage(msg);
      setProcessing(false);
      addLog('error', `Export WebSocket error: ${msg}`);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === 'export_complete') {
          const data = msg.data;
          const exportPath = data.export_path || 'data/processed';
          setCurrentStage('Export Complete!');
          setProgress(100);
          setMessage(`Clips saved to: ${exportPath}`);
          setProcessing(false);
          addLog('success', `Export complete. Files saved to: ${exportPath}`);
          ws.close();
        }
      } catch {
        // ignore
      }
    };

    ws.onopen = async () => {
      try {
        setProgress(30);
        setMessage('Sending export request...');

        const response = await fetch(`${BACKEND}/api/export`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ clip_ids: clipIds }),
        });

        if (!response.ok) {
          throw new Error('Export request failed');
        }

        setProgress(60);
        setMessage('Export in progress, please wait...');
        addLog('info', 'Export request sent. Waiting for completion...');

        // Fallback: query export dir if no WebSocket message within 10s
        setTimeout(async () => {
          if (!processing) return;
          try {
            const dirRes = await fetch(`${BACKEND}/api/export/directory`);
            if (dirRes.ok) {
              const { path } = await dirRes.json();
              setCurrentStage('Export Complete!');
              setProgress(100);
              setMessage(`Clips saved to: ${path}`);
              addLog('success', `Export complete. Files saved to: ${path}`);
            } else {
              setCurrentStage('Export Complete!');
              setProgress(100);
              setMessage('Clips exported successfully.');
              addLog('success', 'Export complete.');
            }
          } catch {
            setCurrentStage('Export Complete!');
            setProgress(100);
            setMessage('Clips exported successfully.');
            addLog('success', 'Export complete.');
          }
          setProcessing(false);
          ws.close();
        }, 10000);
      } catch (error) {
        const errMsg = error instanceof Error ? error.message : 'Export failed';
        setCurrentStage('Export Error');
        setMessage(errMsg);
        setProcessing(false);
        addLog('error', `Export error: ${errMsg}`);
        ws.close();
      }
    };
  }, [selectedClips, processing, addLog]);

  const toggleClipSelection = (id: string) => {
    const newSelected = new Set(selectedClips);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedClips(newSelected);
  };

  const selectAllClips = () => setSelectedClips(new Set(clips.map((c) => c.id as string)));
  const deselectAllClips = () => setSelectedClips(new Set<string>());

  // Show backend startup screen until health check passes
  if (!backendReady) {
    return <BackendSplash timedOut={timedOut} onRetry={retry} />;
  }

  if (showOnboarding) {
    return <ApiKeySetup onComplete={handleOnboardingComplete} />;
  }

  return (
    <>
      <MainLayout
        url={url}
        setUrl={setUrl}
        isUrlValid={isUrlValid}
        setIsUrlValid={setIsUrlValid}
        processing={processing}
        currentStage={currentStage}
        progress={progress}
        message={message}
        clips={clips}
        selectedClips={selectedClips}
        toggleClipSelection={toggleClipSelection}
        selectAllClips={selectAllClips}
        deselectAllClips={deselectAllClips}
        handleGenerate={handleGenerate}
        handleExport={handleExport}
        onOpenSettings={() => setShowSettings(true)}
        logEntries={logEntries}
        logUnread={logUnread}
        onClearLog={clearLog}
        onMarkLogRead={markRead}
      />

      {showSettings && <SettingsPanel onClose={handleSettingsClose} />}
    </>
  );
}

export default App;

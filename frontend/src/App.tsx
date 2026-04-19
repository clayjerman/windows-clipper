import { useState, useEffect } from 'react';
import MainLayout from './components/Layout/MainLayout';
import { ApiKeySetup } from './components/Onboarding';
import { SettingsPanel } from './components/Settings';
import { hasApiKeys } from './services/settingsStorage';

function App() {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [isSetupComplete, setIsSetupComplete] = useState(false);

  // State for video processing
  const [url, setUrl] = useState('');
  const [isUrlValid, setIsUrlValid] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState('');
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  // State for clips
  const [clips, setClips] = useState<any[]>([]);
  const [selectedClips, setSelectedClips] = useState<Set<number>>(new Set());

  // Check if user has set up API keys
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
    // Re-check API keys status after settings close
    const hasKeys = hasApiKeys();
    if (!hasKeys && isSetupComplete) {
      setShowOnboarding(true);
    }
  };

  const handleGenerate = () => {
    if (!isUrlValid) return;
    setProcessing(true);
    setCurrentStage('Downloading video...');
    setProgress(10);
    setMessage('Fetching video from YouTube...');

    // Simulate processing
    setTimeout(() => {
      setCurrentStage('Transcribing audio...');
      setProgress(30);
      setMessage('Converting speech to text...');

      setTimeout(() => {
        setCurrentStage('Analyzing content...');
        setProgress(60);
        setMessage('Identifying viral moments...');

        setTimeout(() => {
          setCurrentStage('Generating clips...');
          setProgress(85);
          setMessage('Creating video clips...');

          // Add some dummy clips
          setClips([
            { id: 1, title: 'Viral Moment 1', duration: 30, score: 95, thumbnail: '' },
            { id: 2, title: 'Viral Moment 2', duration: 30, score: 88, thumbnail: '' },
            { id: 3, title: 'Viral Moment 3', duration: 30, score: 82, thumbnail: '' },
          ]);

          setTimeout(() => {
            setCurrentStage('Complete!');
            setProgress(100);
            setMessage('Your clips are ready!');
            setProcessing(false);
          }, 2000);
        }, 2000);
      }, 2000);
    }, 2000);
  };

  const toggleClipSelection = (id: number) => {
    const newSelected = new Set(selectedClips);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedClips(newSelected);
  };

  const handleExport = () => {
    if (selectedClips.size === 0) return;

    setProcessing(true);
    setCurrentStage('Exporting...');
    setProgress(50);
    setMessage('Preparing video files...');

    setTimeout(() => {
      setCurrentStage('Complete!');
      setProgress(100);
      setMessage('Clips exported successfully!');
      setProcessing(false);
    }, 2000);
  };

  // If showing onboarding, render onboarding screen
  if (showOnboarding) {
    return <ApiKeySetup onComplete={handleOnboardingComplete} />;
  }

  return (
    <>
      {/* Main Application */}
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
        handleGenerate={handleGenerate}
        handleExport={handleExport}
        onOpenSettings={() => setShowSettings(true)}
      />

      {/* Settings Modal */}
      {showSettings && (
        <SettingsPanel onClose={handleSettingsClose} />
      )}
    </>
  );
}

export default App;

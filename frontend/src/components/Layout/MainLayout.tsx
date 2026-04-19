import { useState } from 'react';
import { Settings as SettingsIcon, ScrollText } from 'lucide-react';
import LeftPanel from './LeftPanel';
import CenterPanel from './CenterPanel';
import RightPanel from './RightPanel';
import LogPanel from '../Log/LogPanel';
import type { LogEntry } from '../../hooks/useLog';

interface MainLayoutProps {
  url: string;
  setUrl: (url: string) => void;
  isUrlValid: boolean;
  setIsUrlValid: (valid: boolean) => void;
  processing: boolean;
  currentStage: string;
  progress: number;
  message: string;
  clips: any[];
  selectedClips: Set<string>;
  toggleClipSelection: (id: string) => void;
  selectAllClips: () => void;
  deselectAllClips: () => void;
  handleGenerate: () => void;
  handleExport: () => void;
  onOpenSettings: () => void;
  logEntries: LogEntry[];
  logUnread: number;
  onClearLog: () => void;
  onMarkLogRead: () => void;
}

export default function MainLayout({
  url,
  setUrl,
  isUrlValid,
  setIsUrlValid,
  processing,
  currentStage,
  progress,
  message,
  clips,
  selectedClips,
  toggleClipSelection,
  selectAllClips,
  deselectAllClips,
  handleGenerate,
  handleExport,
  onOpenSettings,
  logEntries,
  logUnread,
  onClearLog,
  onMarkLogRead,
}: MainLayoutProps) {
  const [selectedClip, setSelectedClip] = useState<any>(null);
  const [showLog, setShowLog] = useState(false);

  const toggleLog = () => {
    setShowLog((v) => {
      if (!v) onMarkLogRead();
      return !v;
    });
  };

  return (
    <div className="h-screen flex flex-col bg-[#0A0A0C]">
      {/* Top Bar */}
      <header className="h-14 border-b border-white/10 bg-[#0D0D0F] flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-[#8B5CF6] to-[#EC4899] rounded-lg flex items-center justify-center">
            <svg
              className="w-5 h-5 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h1 className="text-lg font-bold text-white">AI Clipper</h1>
        </div>

        <div className="flex items-center gap-1">
          {/* Log button */}
          <button
            onClick={toggleLog}
            title="Activity log"
            className={`relative p-2 rounded-lg transition-colors ${
              showLog
                ? 'bg-white/10 text-white'
                : 'text-gray-500 hover:text-gray-300 hover:bg-white/5'
            }`}
          >
            <ScrollText className="w-4 h-4" />
            {logUnread > 0 && (
              <span className="absolute -top-0.5 -right-0.5 min-w-[14px] h-[14px] px-[3px] rounded-full bg-[#8B5CF6] text-white text-[9px] font-bold flex items-center justify-center leading-none">
                {logUnread > 99 ? '99+' : logUnread}
              </span>
            )}
          </button>

          {/* Settings button */}
          <button
            onClick={onOpenSettings}
            className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 transition-colors text-gray-300 hover:text-white"
            title="Settings"
          >
            <SettingsIcon className="w-5 h-5" />
            <span className="text-sm">Settings</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <LeftPanel
          url={url}
          setUrl={setUrl}
          setIsUrlValid={setIsUrlValid}
          isUrlValid={isUrlValid}
          processing={processing}
          setProcessing={() => {}}
          currentStage={currentStage}
          progress={progress}
          handleGenerate={handleGenerate}
        />

        <CenterPanel
          url={url}
          processing={processing}
          currentStage={currentStage}
          progress={progress}
          message={message}
          selectedClip={selectedClip}
          setSelectedClip={setSelectedClip}
        />

        <RightPanel
          clips={clips}
          selectedClips={selectedClips}
          toggleClipSelection={toggleClipSelection}
          selectAllClips={selectAllClips}
          deselectAllClips={deselectAllClips}
          handleExport={handleExport}
          processing={processing}
          selectedClip={selectedClip}
          setSelectedClip={setSelectedClip}
        />
      </div>

      {/* Log Panel overlay */}
      {showLog && (
        <LogPanel
          entries={logEntries}
          onClose={() => setShowLog(false)}
          onClear={onClearLog}
        />
      )}
    </div>
  );
}

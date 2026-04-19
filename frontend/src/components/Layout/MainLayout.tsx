import { useState } from 'react';
import { Settings as SettingsIcon } from 'lucide-react';
import LeftPanel from './LeftPanel';
import CenterPanel from './CenterPanel';
import RightPanel from './RightPanel';

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
  selectedClips: Set<number>;
  toggleClipSelection: (id: number) => void;
  handleGenerate: () => void;
  handleExport: () => void;
  onOpenSettings: () => void;
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
  handleGenerate,
  handleExport,
  onOpenSettings,
}: MainLayoutProps) {
  const [selectedClip, setSelectedClip] = useState<any>(null);
  const [processingState, setProcessingState] = useState(processing);
  const [currentStageState, setCurrentStage] = useState(currentStage);
  const [progressState, setProgressState] = useState(progress);
  const [messageState, setMessageState] = useState(message);

  // Update state when props change
  if (processingState !== processing) setProcessingState(processing);
  if (currentStageState !== currentStage) setCurrentStage(currentStage);
  if (progressState !== progress) setProgressState(progress);
  if (messageState !== message) setMessageState(message);

  const handleGenerateClick = () => {
    handleGenerate();
  };

  const handleExportClick = () => {
    handleExport();
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

        <button
          onClick={onOpenSettings}
          className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 transition-colors text-gray-300 hover:text-white"
          title="Settings"
        >
          <SettingsIcon className="w-5 h-5" />
          <span className="text-sm">Settings</span>
        </button>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <LeftPanel
          url={url}
          setUrl={setUrl}
          setIsUrlValid={setIsUrlValid}
          isUrlValid={isUrlValid}
          processing={processingState}
          setProcessing={() => {}}
          currentStage={currentStageState}
          progress={progressState}
          handleGenerate={handleGenerateClick}
        />

        <CenterPanel
          url={url}
          processing={processingState}
          currentStage={currentStageState}
          progress={progressState}
          message={messageState}
          selectedClip={selectedClip}
          setSelectedClip={setSelectedClip}
        />

        <RightPanel
          clips={clips}
          selectedClips={selectedClips}
          toggleClipSelection={toggleClipSelection}
          handleExport={handleExportClick}
          processing={processingState}
          selectedClip={selectedClip}
          setSelectedClip={setSelectedClip}
        />
      </div>
    </div>
  );
}

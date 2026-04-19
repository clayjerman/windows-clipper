import { useState } from 'react';
import { Link2, Loader2 } from 'lucide-react';
import URLInput from '../Input/URLInput';
import SettingsPanel from '../Input/SettingsPanel';
import GenerateButton from '../Input/GenerateButton';

interface LeftPanelProps {
  url: string;
  setUrl: (url: string) => void;
  setIsUrlValid: (valid: boolean) => void;
  isUrlValid: boolean;
  processing: boolean;
  setProcessing: (processing: boolean) => void;
  currentStage: string;
  progress: number;
  handleGenerate: () => void;
}

export default function LeftPanel({
  url,
  setUrl,
  setIsUrlValid,
  isUrlValid,
  processing,
  setProcessing,
  currentStage,
  progress,
  handleGenerate
}: LeftPanelProps) {
  const [clipDuration, setClipDuration] = useState(30);
  const [numberOfClips, setNumberOfClips] = useState(5);
  const [subtitleStyle, setSubtitleStyle] = useState('default');
  const [enableSubtitles, setEnableSubtitles] = useState(true);
  const [enableJumpCuts, setEnableJumpCuts] = useState(true);

  return (
    <div className="w-80 border-r border-white/10 bg-[#0D0D0F] flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-8 h-8 bg-[#8B5CF6] rounded-lg flex items-center justify-center">
            <Link2 className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-lg font-bold text-white">AI Clipper</h1>
        </div>
        <p className="text-xs text-gray-400">Generate viral clips from YouTube</p>
      </div>

      {/* URL Input */}
      <div className="p-4 border-b border-white/10">
        <URLInput url={url} setUrl={setUrl} setIsUrlValid={setIsUrlValid} />
      </div>

      {/* Settings */}
      <SettingsPanel
        clipDuration={clipDuration}
        setClipDuration={setClipDuration}
        numberOfClips={numberOfClips}
        setNumberOfClips={setNumberOfClips}
        subtitleStyle={subtitleStyle}
        setSubtitleStyle={setSubtitleStyle}
        enableSubtitles={enableSubtitles}
        setEnableSubtitles={setEnableSubtitles}
        enableJumpCuts={enableJumpCuts}
        setEnableJumpCuts={setEnableJumpCuts}
      />

      {/* Generate Button */}
      <div className="p-4 mt-auto">
        <GenerateButton
          processing={processing}
          onClick={handleGenerate}
        />

        {/* Processing Status */}
        {processing && (
          <div className="mt-4 p-3 bg-[#1A1A1D] rounded-lg">
            <div className="flex items-center gap-2 text-sm text-white mb-2">
              <Loader2 className="w-4 h-4 animate-spin text-[#8B5CF6]" />
              <span className="font-medium">{currentStage}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-[#8B5CF6] h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-xs text-gray-400 mt-1">{Math.round(progress)}%</p>
          </div>
        )}
      </div>
    </div>
  );
}

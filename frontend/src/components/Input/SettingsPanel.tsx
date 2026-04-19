import { Settings } from 'lucide-react';
import { useState } from 'react';

interface SettingsPanelProps {
  clipDuration: number;
  setClipDuration: (duration: number) => void;
  numberOfClips: number;
  setNumberOfClips: (count: number) => void;
  subtitleStyle: string;
  setSubtitleStyle: (style: string) => void;
  enableSubtitles: boolean;
  setEnableSubtitles: (enabled: boolean) => void;
  enableJumpCuts: boolean;
  setEnableJumpCuts: (enabled: boolean) => void;
}

export default function SettingsPanel({
  clipDuration,
  setClipDuration,
  numberOfClips,
  setNumberOfClips,
  subtitleStyle,
  setSubtitleStyle,
  enableSubtitles,
  setEnableSubtitles,
  enableJumpCuts,
  setEnableJumpCuts,
}: SettingsPanelProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border-t border-white/10 bg-[#0D0D0F]">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex items-center justify-between text-white hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Settings className="w-4 h-4 text-gray-400" />
          <span className="text-sm font-medium">Settings</span>
        </div>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${
            expanded ? 'rotate-180' : ''
          }`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {expanded && (
        <div className="px-4 py-3 space-y-4 border-t border-white/10">
          {/* Clip Duration */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Clip Duration: {clipDuration}s
            </label>
            <input
              type="range"
              min="15"
              max="60"
              step="5"
              value={clipDuration}
              onChange={(e) => setClipDuration(Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Number of Clips */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Number of Clips: {numberOfClips}
            </label>
            <input
              type="range"
              min="1"
              max="10"
              step="1"
              value={numberOfClips}
              onChange={(e) => setNumberOfClips(Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Subtitle Style */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Subtitle Style
            </label>
            <select
              value={subtitleStyle}
              onChange={(e) => setSubtitleStyle(e.target.value)}
              className="w-full bg-[#1A1A1D] border border-white/10 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#8B5CF6]"
            >
              <option value="default">Default</option>
              <option value="tiktok">TikTok Style</option>
              <option value="youtube">YouTube Style</option>
              <option value="custom">Custom</option>
            </select>
          </div>

          {/* Toggle Switches */}
          <div className="space-y-2">
            <label className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Enable Subtitles</span>
              <input
                type="checkbox"
                checked={enableSubtitles}
                onChange={(e) => setEnableSubtitles(e.target.checked)}
                className="sr-only peer"
              />
              <div className="relative w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#8B5CF6]" />
            </label>

            <label className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Enable Jump Cuts</span>
              <input
                type="checkbox"
                checked={enableJumpCuts}
                onChange={(e) => setEnableJumpCuts(e.target.checked)}
                className="sr-only peer"
              />
              <div className="relative w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#8B5CF6]" />
            </label>
          </div>
        </div>
      )}
    </div>
  );
}

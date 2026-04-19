import { Play } from 'lucide-react';
import { VideoPlayer } from '../Video/VideoPlayer';

interface CenterPanelProps {
  url: string;
  processing: boolean;
  currentStage: string;
  progress: number;
  message: string;
  selectedClip: any;
  setSelectedClip: (clip: any) => void;
}

export default function CenterPanel({
  url,
  processing,
  currentStage,
  progress,
  message,
  selectedClip,
}: CenterPanelProps) {
  return (
    <div className="flex-1 flex flex-col bg-[#0A0A0C]">
      {/* Video Player Container */}
      <div className="flex-1 flex items-center justify-center p-8 overflow-hidden">
        {selectedClip ? (
          <div className="flex flex-col items-center h-full max-h-full">
            {/* Vertical clip preview */}
            <div className="flex-1 min-h-0 flex items-center justify-center">
              <VideoPlayer
                src={selectedClip.videoUrl}
                thumbnail={selectedClip.thumbnail}
                className="h-full max-h-full w-auto aspect-[9/16]"
              />
            </div>
            <div className="mt-4 p-4 bg-[#0D0D0F] rounded-lg w-full max-w-sm">
              <h2 className="text-base font-semibold text-white mb-1 truncate">
                {selectedClip.title}
              </h2>
              <div className="flex items-center gap-3 text-sm text-gray-400">
                <span>{selectedClip.duration}s</span>
                <span>•</span>
                <span className="text-green-400 font-medium">{selectedClip.score}% viral score</span>
              </div>
              {selectedClip.description && (
                <p className="text-xs text-gray-500 mt-2 line-clamp-2">
                  {selectedClip.description}
                </p>
              )}
            </div>
          </div>
        ) : url ? (
          <div className="w-full max-w-4xl">
            <div className="aspect-video bg-[#1A1A1D] rounded-lg flex items-center justify-center">
              <Play className="w-16 h-16 text-[#8B5CF6]/50" />
            </div>
            <div className="mt-4 p-4 bg-[#0D0D0F] rounded-lg">
              <h2 className="text-lg font-semibold text-white mb-2">YouTube Video</h2>
              <p className="text-sm text-gray-400 break-all">{url}</p>
            </div>
          </div>
        ) : (
          <div className="text-center">
            <div className="w-24 h-24 bg-[#1A1A1D] rounded-full flex items-center justify-center mb-4">
              <Play className="w-12 h-12 text-[#8B5CF6]/50" />
            </div>
            <h2 className="text-xl font-semibold text-white mb-2">No Video Selected</h2>
            <p className="text-gray-400">Paste a YouTube URL to get started</p>
          </div>
        )}
      </div>

      {/* Processing Progress */}
      {(processing || message) && (
        <div className="p-4 border-t border-white/10 bg-[#0D0D0F]">
          <div className="max-w-4xl mx-auto">
            {processing && (
              <>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-white">{currentStage}</span>
                  <span className="text-sm text-[#8B5CF6]">{Math.round(progress)}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-[#8B5CF6] h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </>
            )}
            {message && (
              <p
                className={`text-xs mt-2 ${
                  message.startsWith('Clips saved')
                    ? 'text-green-400 font-medium'
                    : message.includes('Error') || message.includes('Cannot')
                    ? 'text-red-400'
                    : 'text-gray-400'
                }`}
              >
                {message}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

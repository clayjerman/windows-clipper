import { CheckCircle, Loader2 } from 'lucide-react';
import { ProcessingProgress } from '../../types/api';

interface ProcessingProgressBarProps {
  progress: ProcessingProgress;
}

const stageMessages: Record<string, string> = {
  downloading: 'Downloading video...',
  transcribing: 'Transcribing audio...',
  analyzing: 'Analyzing content...',
  detecting: 'Detecting speakers...',
  editing: 'Generating clips...',
  complete: 'Complete!',
};

export default function ProcessingProgressBar({ progress }: ProcessingProgressBarProps) {
  const stageMessage = stageMessages[progress.stage] || progress.message || 'Processing...';
  const percentage = Math.round(progress.progress);

  return (
    <div className="bg-[#0D0D0F] rounded-lg p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {progress.stage === 'complete' ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : (
            <Loader2 className="w-5 h-5 text-[#8B5CF6] animate-spin" />
          )}
          <span className="text-sm font-medium text-white">{stageMessage}</span>
        </div>
        <span className="text-sm font-bold text-[#8B5CF6]">{percentage}%</span>
      </div>

      <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
        <div
          className="bg-[#8B5CF6] h-2 rounded-full transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {progress.details && (
        <div className="text-xs text-gray-400 space-y-1">
          {progress.details.message && <p>{progress.details.message}</p>}
          {progress.current_clip !== undefined && progress.total_clips !== undefined && (
            <p>
              Clip {progress.current_clip} of {progress.total_clips}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

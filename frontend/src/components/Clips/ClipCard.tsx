import { useState } from 'react';
import { Play, Check, Star, Clock, Flame } from 'lucide-react';

interface ClipCardProps {
  clip: any;
  selected: boolean;
  toggleSelection: () => void;
  isSelectedClip: boolean;
  onClick: () => void;
  listView?: boolean;
}

export default function ClipCard({
  clip,
  selected,
  toggleSelection,
  isSelectedClip,
  onClick,
  listView = false,
}: ClipCardProps) {
  const [hovered, setHovered] = useState(false);

  const getScoreColor = (score: number): string => {
    if (score >= 90) return 'text-green-400';
    if (score >= 70) return 'text-yellow-400';
    return 'text-orange-400';
  };

  const getScoreLabel = (score: number): string => {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Good';
    return 'Fair';
  };

  if (listView) {
    return (
      <div
        onClick={onClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        className={`p-3 rounded-lg border transition-all cursor-pointer ${
          isSelectedClip
            ? 'border-[#8B5CF6] bg-[#8B5CF6]/10'
            : hovered
            ? 'border-gray-600 bg-[#1A1A1D]'
            : 'border-transparent bg-[#0D0D0F]'
        }`}
      >
        <div className="flex items-center gap-3">
          {/* Checkbox */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleSelection();
            }}
            className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
              selected
                ? 'bg-[#8B5CF6] border-[#8B5CF6]'
                : 'border-gray-600 hover:border-gray-500'
            }`}
          >
            {selected && <Check className="w-3 h-3 text-white" />}
          </button>

          {/* Thumbnail */}
          <div className="w-24 h-14 bg-[#1A1A1D] rounded flex items-center justify-center relative overflow-hidden group">
            <Play className="w-6 h-6 text-white/50 group-hover:text-white/80 transition-colors" />
            {hovered && (
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                <Play className="w-8 h-8 text-white" />
              </div>
            )}
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-semibold text-white truncate">{clip.title}</h3>
            <div className="flex items-center gap-3 mt-1">
              <span className="text-xs text-gray-400 flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {clip.duration}s
              </span>
              <span className={`text-xs font-medium flex items-center gap-1 ${getScoreColor(clip.score)}`}>
                <Flame className="w-3 h-3" />
                {clip.score}% {getScoreLabel(clip.score)}
              </span>
            </div>
          </div>

          {/* Score Badge */}
          <div className={`px-3 py-1 rounded-full text-xs font-bold ${getScoreColor(clip.score)}`}>
            {clip.score}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`relative group rounded-lg overflow-hidden border-2 transition-all cursor-pointer ${
        isSelectedClip
          ? 'border-[#8B5CF6]'
          : hovered
          ? 'border-gray-600'
          : 'border-transparent'
      }`}
    >
      {/* Thumbnail */}
      <div className="aspect-[9/16] bg-[#1A1A1D] flex items-center justify-center relative overflow-hidden">
        <Play className="w-12 h-12 text-white/30 group-hover:text-white/50 transition-colors" />

        {/* Hover Overlay */}
        {hovered && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <Play className="w-16 h-16 text-white" />
          </div>
        )}

        {/* Duration Badge */}
        <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/70 rounded text-white text-xs font-medium">
          {clip.duration}s
        </div>

        {/* Score Badge */}
        <div className={`absolute top-2 left-2 px-2 py-1 bg-black/70 rounded text-xs font-bold ${getScoreColor(clip.score)}`}>
          {clip.score}%
        </div>
      </div>

      {/* Info */}
      <div className="p-3 bg-[#0D0D0F]">
        {/* Checkbox */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleSelection();
          }}
          className={`absolute top-3 right-3 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors z-10 ${
            selected
              ? 'bg-[#8B5CF6] border-[#8B5CF6]'
              : 'border-gray-600 hover:border-gray-500 bg-black/50'
          }`}
        >
          {selected && <Check className="w-3 h-3 text-white" />}
        </button>

        <h3 className="text-sm font-semibold text-white truncate pr-8">{clip.title}</h3>

        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-gray-400 flex items-center gap-1">
            <Flame className="w-3 h-3" />
            {getScoreLabel(clip.score)}
          </span>
          <span className={`text-xs font-bold ${getScoreColor(clip.score)}`}>
            {clip.score}/100
          </span>
        </div>
      </div>
    </div>
  );
}

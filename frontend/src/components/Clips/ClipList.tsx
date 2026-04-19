import { useState } from 'react';
import { Grid, List, Filter, ChevronDown } from 'lucide-react';
import ClipCard from './ClipCard';

interface ClipListProps {
  clips: any[];
  selectedClips: Set<number>;
  toggleClipSelection: (id: number) => void;
  viewMode: 'grid' | 'list';
  selectedClip: any;
  setSelectedClip: (clip: any) => void;
}

export default function ClipList({
  clips,
  selectedClips,
  toggleClipSelection,
  viewMode,
  selectedClip,
  setSelectedClip
}: ClipListProps) {
  const [sortBy, setSortBy] = useState('score');

  return (
    <div className="space-y-3">
      {/* Statistics Bar */}
      <div className="flex items-center justify-between p-3 bg-[#1A1A1D] rounded-lg">
        <div className="flex items-center gap-4">
          <div>
            <p className="text-xs text-gray-400">Total Clips</p>
            <p className="text-lg font-bold text-white">{clips.length}</p>
          </div>
          <div className="w-px h-8 bg-gray-700"></div>
          <div>
            <p className="text-xs text-gray-400">Selected</p>
            <p className="text-lg font-bold text-[#8B5CF6]">{selectedClips.size}</p>
          </div>
          <div className="w-px h-8 bg-gray-700"></div>
          <div>
            <p className="text-xs text-gray-400">Avg Score</p>
            <p className="text-lg font-bold text-green-400">
              {clips.length > 0
                ? Math.round(clips.reduce((sum, c) => sum + c.score, 0) / clips.length)
                : 0}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1 px-2 py-1.5 rounded bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 transition-colors text-sm">
            <Filter className="w-3 h-3" />
            <span>{sortBy === 'score' ? 'Score' : sortBy === 'duration' ? 'Duration' : 'Latest'}</span>
            <ChevronDown className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Clips */}
      {clips.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-[#1A1A1D] rounded-full flex items-center justify-center mx-auto mb-4">
            <Grid className="w-8 h-8 text-gray-600" />
          </div>
          <p className="text-gray-400 mb-2">No clips generated yet</p>
          <p className="text-sm text-gray-500">
            Paste a YouTube URL and click "Generate Clips"
          </p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-2 gap-3">
          {clips.map((clip) => (
            <ClipCard
              key={clip.id}
              clip={clip}
              selected={selectedClips.has(clip.id)}
              toggleSelection={() => toggleClipSelection(clip.id)}
              isSelectedClip={selectedClip?.id === clip.id}
              onClick={() => setSelectedClip(clip)}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {clips.map((clip) => (
            <ClipCard
              key={clip.id}
              clip={clip}
              selected={selectedClips.has(clip.id)}
              toggleSelection={() => toggleClipSelection(clip.id)}
              isSelectedClip={selectedClip?.id === clip.id}
              onClick={() => setSelectedClip(clip)}
              listView
            />
          ))}
        </div>
      )}
    </div>
  );
}

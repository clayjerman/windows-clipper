import { useState } from 'react';
import { Download, Share2, Filter, Grid, List, ChevronDown } from 'lucide-react';
import ClipList from '../Clips/ClipList';

interface RightPanelProps {
  clips: any[];
  selectedClips: Set<string>;
  toggleClipSelection: (id: string) => void;
  selectAllClips: () => void;
  deselectAllClips: () => void;
  handleExport: () => void;
  processing: boolean;
  selectedClip: any;
  setSelectedClip: (clip: any) => void;
}

export default function RightPanel({
  clips,
  selectedClips,
  toggleClipSelection,
  selectAllClips,
  deselectAllClips,
  handleExport,
  processing,
  selectedClip,
  setSelectedClip,
}: RightPanelProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const selectedCount = selectedClips.size;
  const allSelected = clips.length > 0 && selectedCount === clips.length;
  const canExport = selectedCount > 0 && !processing;

  return (
    <div className="w-96 border-l border-white/10 bg-[#0D0D0F] flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-white/10">
        <h2 className="text-lg font-bold text-white mb-1">Generated Clips</h2>
        <p className="text-xs text-gray-400">
          {clips.length > 0
            ? `${clips.length} clip${clips.length > 1 ? 's' : ''} generated`
            : 'No clips generated yet'}
        </p>
      </div>

      {/* Toolbar */}
      <div className="p-4 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-lg transition-colors ${
              viewMode === 'grid'
                ? 'bg-[#8B5CF6]/20 text-[#8B5CF6]'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
            title="Grid View"
          >
            <Grid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-lg transition-colors ${
              viewMode === 'list'
                ? 'bg-[#8B5CF6]/20 text-[#8B5CF6]'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
            title="List View"
          >
            <List className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white/5 text-gray-300 hover:bg-white/10 transition-colors text-sm">
            <Filter className="w-4 h-4" />
            <span>Sort</span>
            <ChevronDown className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Clip List */}
      <div className="flex-1 overflow-y-auto p-4">
        <ClipList
          clips={clips}
          selectedClips={selectedClips}
          toggleClipSelection={toggleClipSelection}
          viewMode={viewMode}
          selectedClip={selectedClip}
          setSelectedClip={setSelectedClip}
        />
      </div>

      {/* Export Bar */}
      {clips.length > 0 && (
        <div className="p-4 border-t border-white/10 bg-[#0D0D0F]">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="selectAll"
                checked={allSelected}
                onChange={() => (allSelected ? deselectAllClips() : selectAllClips())}
                className="w-4 h-4 rounded border-gray-600 bg-[#0D0D0F] text-[#8B5CF6] focus:ring-[#8B5CF6]"
              />
              <label htmlFor="selectAll" className="text-sm text-gray-300 cursor-pointer">
                Select All ({selectedCount}/{clips.length})
              </label>
            </div>
          </div>

          <button
            onClick={handleExport}
            disabled={!canExport}
            className="w-full px-4 py-3 rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#EC4899] text-white font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {processing ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Exporting...
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                Export {selectedCount > 0 ? `${selectedCount} Clip${selectedCount > 1 ? 's' : ''}` : 'All'}
              </>
            )}
          </button>

          {canExport && (
            <div className="mt-2 flex gap-2">
              <button className="flex-1 px-3 py-2 rounded-lg border border-white/10 text-gray-300 hover:bg-white/5 transition-colors flex items-center justify-center gap-2 text-sm">
                <Share2 className="w-4 h-4" />
                Share
              </button>
              <button className="flex-1 px-3 py-2 rounded-lg border border-white/10 text-gray-300 hover:bg-white/5 transition-colors flex items-center justify-center gap-2 text-sm">
                <Download className="w-4 h-4" />
                Download
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

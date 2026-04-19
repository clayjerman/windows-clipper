import { useEffect, useRef } from 'react';
import { X, Trash2 } from 'lucide-react';
import type { LogEntry } from '../../hooks/useLog';

interface LogPanelProps {
  entries: LogEntry[];
  onClose: () => void;
  onClear: () => void;
}

const levelDot: Record<string, string> = {
  success: 'bg-green-400',
  error: 'bg-red-400',
  info: 'bg-blue-400',
};

const levelText: Record<string, string> = {
  success: 'text-green-400',
  error: 'text-red-400',
  info: 'text-blue-400',
};

function formatTime(date: Date) {
  return date.toLocaleTimeString('en-GB', { hour12: false });
}

export default function LogPanel({ entries, onClose, onClear }: LogPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [entries]);

  return (
    <div className="fixed bottom-4 right-4 w-[380px] z-50 flex flex-col rounded-xl border border-white/10 bg-[#0D0D0F] shadow-2xl shadow-black/60 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-white/10 bg-[#111114]">
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <span className="w-2 h-2 rounded-full bg-red-500/70" />
            <span className="w-2 h-2 rounded-full bg-yellow-500/70" />
            <span className="w-2 h-2 rounded-full bg-green-500/70" />
          </div>
          <span className="text-xs font-mono text-gray-400">activity log</span>
          <span className="text-xs text-gray-600">({entries.length})</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={onClear}
            title="Clear log"
            className="p-1 rounded hover:bg-white/5 text-gray-600 hover:text-gray-400 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onClose}
            title="Close"
            className="p-1 rounded hover:bg-white/5 text-gray-600 hover:text-gray-400 transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Entries */}
      <div className="h-64 overflow-y-auto font-mono text-xs p-2 space-y-0.5">
        {entries.length === 0 ? (
          <p className="text-gray-600 text-center py-8">No activity yet.</p>
        ) : (
          entries.map((entry) => (
            <div key={entry.id} className="flex items-start gap-2 py-0.5 px-1 rounded hover:bg-white/[0.03]">
              <span className="text-gray-600 shrink-0 mt-0.5">{formatTime(entry.timestamp)}</span>
              <span className={`shrink-0 mt-[5px] w-1.5 h-1.5 rounded-full ${levelDot[entry.level]}`} />
              <span className={`break-all leading-relaxed ${levelText[entry.level]}`}>
                {entry.message}
              </span>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

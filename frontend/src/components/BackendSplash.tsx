import { useEffect, useState } from 'react';
import { RefreshCw, AlertCircle } from 'lucide-react';

interface BackendSplashProps {
  timedOut: boolean;
  onRetry: () => void;
}

const STAGES = [
  'Starting AI Clipper…',
  'Loading Python environment…',
  'Initialising backend server…',
  'Almost ready… (first launch may take a minute)',
];

export default function BackendSplash({ timedOut, onRetry }: BackendSplashProps) {
  const [stageIdx, setStageIdx] = useState(0);
  const [dots, setDots] = useState('');

  // Cycle through stage messages every ~3 s
  useEffect(() => {
    if (timedOut) return;
    const id = setInterval(() => {
      setStageIdx((i) => Math.min(i + 1, STAGES.length - 1));
    }, 3000);
    return () => clearInterval(id);
  }, [timedOut]);

  // Animate dots
  useEffect(() => {
    if (timedOut) return;
    const id = setInterval(() => {
      setDots((d) => (d.length >= 3 ? '' : d + '.'));
    }, 500);
    return () => clearInterval(id);
  }, [timedOut]);

  return (
    <div className="h-screen w-screen flex flex-col items-center justify-center bg-[#0A0A0C] select-none">
      {/* Logo */}
      <div className="w-16 h-16 bg-gradient-to-br from-[#8B5CF6] to-[#EC4899] rounded-2xl flex items-center justify-center mb-8 shadow-lg shadow-[#8B5CF6]/30">
        <svg className="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      <h1 className="text-2xl font-bold text-white mb-1">AI Clipper</h1>
      <p className="text-sm text-gray-500 mb-10">Generate viral clips from YouTube</p>

      {timedOut ? (
        /* ── Error state ── */
        <div className="flex flex-col items-center gap-4 max-w-xs text-center">
          <AlertCircle className="w-10 h-10 text-red-400" />
          <p className="text-sm text-gray-300 leading-relaxed">
            Backend did not start in time.
            <br />
            Make sure the app was installed correctly and try again.
          </p>
          <button
            onClick={onRetry}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#8B5CF6] hover:bg-[#7C3AED] text-white text-sm font-semibold transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        </div>
      ) : (
        /* ── Loading state ── */
        <div className="flex flex-col items-center gap-5">
          {/* Spinner */}
          <div className="relative w-10 h-10">
            <div className="absolute inset-0 rounded-full border-2 border-white/10" />
            <div className="absolute inset-0 rounded-full border-2 border-t-[#8B5CF6] animate-spin" />
          </div>

          {/* Stage label */}
          <p className="text-sm text-gray-400 w-56 text-center">
            {STAGES[stageIdx]}{dots}
          </p>
        </div>
      )}
    </div>
  );
}

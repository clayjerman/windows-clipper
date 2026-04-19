/**
 * Error toast component
 */

import React, { useEffect } from 'react';
import { XCircle, X } from 'lucide-react';

interface ErrorToastProps {
  message: string;
  onClose: () => void;
  autoClose?: boolean;
  duration?: number;
}

export function ErrorToast({ message, onClose, autoClose = true, duration = 5000 }: ErrorToastProps) {
  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [autoClose, duration, onClose]);

  return (
    <div className="fixed bottom-4 right-4 z-50 animate-slide-up">
      <div className="glass-strong rounded-lg p-4 flex items-start gap-3 shadow-2xl max-w-md">
        <div className="flex-shrink-0 text-red-400">
          <XCircle className="w-5 h-5" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-red-400 font-medium">Error</p>
          <p className="text-sm text-gray-300 mt-1">{message}</p>
        </div>
        <button
          onClick={onClose}
          className="flex-shrink-0 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

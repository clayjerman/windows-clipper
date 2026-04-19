/**
 * Progress bar component
 */

import React from 'react';

interface ProgressBarProps {
  progress: number;
  showLabel?: boolean;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ProgressBar({ progress, showLabel = false, label, size = 'md' }: ProgressBarProps) {
  const heightClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-300">{label}</span>
          {showLabel && (
            <span className="text-sm text-gray-400">{Math.round(progress)}%</span>
          )}
        </div>
      )}
      <div className={`progress-bar ${heightClasses[size]}`}>
        <div
          className="progress-fill transition-all duration-300 ease-out"
          style={{ width: `${Math.min(Math.max(progress, 0), 100)}%` }}
        ></div>
      </div>
    </div>
  );
}

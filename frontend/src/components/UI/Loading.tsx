/**
 * Loading component
 */

import React from 'react';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

export function Loading({ size = 'md', text }: LoadingProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <div className={`${sizeClasses[size]} spinner`}></div>
      {text && <p className="text-sm text-gray-400">{text}</p>}
    </div>
  );
}

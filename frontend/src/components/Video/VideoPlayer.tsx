/**
 * Video player component
 */

import React, { useRef, useEffect, useState } from 'react';
import { Play, Pause, Volume2, VolumeX, Maximize, RotateCcw } from 'lucide-react';

interface VideoPlayerProps {
  src?: string;
  thumbnail?: string;
  onTimeUpdate?: (time: number) => void;
  onPlay?: () => void;
  onPause?: () => void;
  className?: string;
}

export function VideoPlayer({
  src,
  thumbnail,
  onTimeUpdate,
  onPlay,
  onPause,
  className = '',
}: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
      onTimeUpdate?.(video.currentTime);
    };

    const handleLoadedMetadata = () => {
      setDuration(video.duration);
      setIsLoaded(true);
    };

    const handlePlay = () => {
      setIsPlaying(true);
      onPlay?.();
    };

    const handlePause = () => {
      setIsPlaying(false);
      onPause?.();
    };

    const handleEnded = () => {
      setIsPlaying(false);
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('ended', handleEnded);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('ended', handleEnded);
    };
  }, [onTimeUpdate, onPlay, onPause]);

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }
  };

  const toggleMute = () => {
    const video = videoRef.current;
    if (!video) return;

    video.muted = !video.muted;
    setIsMuted(video.muted);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const video = videoRef.current;
    if (!video) return;

    const time = parseFloat(e.target.value);
    video.currentTime = time;
    setCurrentTime(time);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className={`relative bg-dark-900 rounded-xl overflow-hidden ${className}`}>
      {/* Thumbnail overlay when video not loaded */}
      {!src && thumbnail && (
        <div className="absolute inset-0 flex items-center justify-center">
          <img
            src={thumbnail}
            alt="Video thumbnail"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
            <div className="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Play className="w-10 h-10 text-white ml-1" />
            </div>
          </div>
        </div>
      )}

      {/* Video element */}
      <video
        ref={videoRef}
        src={src}
        className="w-full h-full object-contain"
        poster={thumbnail}
      />

      {/* Controls */}
      {isLoaded && src && (
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-200 flex flex-col justify-end p-4">
          {/* Progress bar */}
          <div className="mb-3">
            <input
              type="range"
              min="0"
              max={duration}
              step="0.1"
              value={currentTime}
              onChange={handleSeek}
              className="w-full h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer accent-primary-500"
            />
            <div className="flex justify-between mt-1">
              <span className="text-xs text-gray-300">{formatTime(currentTime)}</span>
              <span className="text-xs text-gray-300">{formatTime(duration)}</span>
            </div>
          </div>

          {/* Control buttons */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                onClick={togglePlay}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                {isPlaying ? (
                  <Pause className="w-5 h-5 text-white" />
                ) : (
                  <Play className="w-5 h-5 text-white ml-0.5" />
                )}
              </button>

              <button
                onClick={toggleMute}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                {isMuted ? (
                  <VolumeX className="w-5 h-5 text-white" />
                ) : (
                  <Volume2 className="w-5 h-5 text-white" />
                )}
              </button>

              <button
                onClick={() => {
                  const video = videoRef.current;
                  if (video) {
                    video.currentTime = 0;
                  }
                }}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                <RotateCcw className="w-5 h-5 text-white" />
              </button>
            </div>

            <button className="p-2 rounded-lg hover:bg-white/10 transition-colors">
              <Maximize className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      )}

      {/* Loading state */}
      {!isLoaded && src && (
        <div className="absolute inset-0 flex items-center justify-center bg-dark-900">
          <div className="spinner w-10 h-10" />
        </div>
      )}
    </div>
  );
}

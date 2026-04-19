import { useState, useCallback } from 'react';
import { apiClient } from '../services/api';
import { ClipSettings, GenerateResponse, ProcessingProgress } from '../types/api';

export function useVideoProcessing() {
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState<ProcessingProgress>({
    stage: '',
    progress: 0,
    message: '',
  });
  const [jobId, setJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateClips = useCallback(async (url: string, settings: ClipSettings) => {
    try {
      setProcessing(true);
      setError(null);
      setProgress({
        stage: 'initializing',
        progress: 0,
        message: 'Starting...',
      });

      // Get video info
      setProgress({
        stage: 'fetching_info',
        progress: 5,
        message: 'Fetching video information...',
      });

      const videoInfo = await apiClient.getVideoInfo(url);

      // Generate clips
      setProgress({
        stage: 'generating',
        progress: 10,
        message: 'Starting clip generation...',
      });

      const response: GenerateResponse = await apiClient.generateClips({
        url,
        settings,
      });

      setJobId(response.job_id);

      setProgress({
        stage: 'processing',
        progress: 15,
        message: 'Processing video...',
      });

      return { jobId: response.job_id, videoInfo };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate clips';
      setError(errorMessage);
      setProcessing(false);
      throw err;
    }
  }, []);

  const updateProgress = useCallback((newProgress: Partial<ProcessingProgress>) => {
    setProgress((prev) => ({
      ...prev,
      ...newProgress,
    }));

    if (newProgress.stage === 'complete' || newProgress.progress === 100) {
      setProcessing(false);
    }
  }, []);

  const resetProcessing = useCallback(() => {
    setProcessing(false);
    setProgress({
      stage: '',
      progress: 0,
      message: '',
    });
    setJobId(null);
    setError(null);
  }, []);

  return {
    processing,
    progress,
    jobId,
    error,
    generateClips,
    updateProgress,
    resetProcessing,
  };
}

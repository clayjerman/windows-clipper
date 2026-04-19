import { useState, useCallback } from 'react';

export function useVideoProcessing() {
  const [url, setUrl] = useState('');
  const [isUrlValid, setIsUrlValid] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState('');
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  const validateYouTubeURL = useCallback((input: string): boolean => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+/;
    return youtubeRegex.test(input);
  }, []);

  const handleGenerate = useCallback(() => {
    if (!isUrlValid) return;
    setProcessing(true);
    setCurrentStage('Downloading video...');
    setProgress(10);
    setMessage('Fetching video from YouTube...');

    // Simulate processing stages
    setTimeout(() => {
      setCurrentStage('Transcribing audio...');
      setProgress(30);
      setMessage('Converting speech to text using Whisper AI...');

      setTimeout(() => {
        setCurrentStage('Analyzing content...');
        setProgress(60);
        setMessage('Identifying viral moments with Gemini AI...');

        setTimeout(() => {
          setCurrentStage('Detecting speakers...');
          setProgress(75);
          setMessage('Tracking faces and identifying active speakers...');

          setTimeout(() => {
            setCurrentStage('Generating clips...');
            setProgress(90);
            setMessage('Creating video clips with smart cropping...');

            setTimeout(() => {
              setCurrentStage('Complete!');
              setProgress(100);
              setMessage('Your viral clips are ready to preview and export!');
              setProcessing(false);
            }, 2000);
          }, 1500);
        }, 1500);
      }, 2000);
    }, 1500);
  }, [isUrlValid]);

  const resetProcessing = useCallback(() => {
    setProcessing(false);
    setCurrentStage('');
    setProgress(0);
    setMessage('');
  }, []);

  return {
    url,
    setUrl,
    isUrlValid,
    setIsUrlValid,
    processing,
    setProcessing,
    currentStage,
    setCurrentStage,
    progress,
    setProgress,
    message,
    setMessage,
    handleGenerate,
    resetProcessing,
    validateYouTubeURL,
  };
}

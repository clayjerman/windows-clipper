import { useState } from 'react';
import { Link2, Check, X, Loader2 } from 'lucide-react';

interface URLInputProps {
  url: string;
  setUrl: (url: string) => void;
  setIsUrlValid: (valid: boolean) => void;
}

export default function URLInput({ url, setUrl, setIsUrlValid }: URLInputProps) {
  const [isValidating, setIsValidating] = useState(false);
  const [isValid, setIsValidState] = useState(false);
  const [validationError, setValidationError] = useState('');

  const validateYouTubeURL = (input: string): boolean => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+/;
    return youtubeRegex.test(input);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUrl(value);
    setIsValidState(false);
    setIsUrlValid(false);
    setValidationError('');
  };

  const handleBlur = () => {
    if (!url.trim()) {
      setIsValidState(false);
      setIsUrlValid(false);
      setValidationError('');
      return;
    }

    setIsValidating(true);

    // Simulate validation delay
    setTimeout(() => {
      const valid = validateYouTubeURL(url);
      setIsValidState(valid);
      setIsUrlValid(valid);

      if (!valid) {
        setValidationError('Please enter a valid YouTube URL');
      } else {
        setValidationError('');
      }

      setIsValidating(false);
    }, 500);
  };

  return (
    <div className="space-y-2">
      <div className="relative">
        <div className="absolute left-3 top-1/2 -translate-y-1/2">
          <Link2 className="w-4 h-4 text-gray-400" />
        </div>

        <input
          type="text"
          value={url}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Paste YouTube URL here..."
          className={`w-full bg-[#0D0D0F] border rounded-lg pl-10 pr-10 py-3 text-white placeholder-gray-500 focus:outline-none transition-colors ${
            url && isValid
              ? 'border-green-500'
              : url && validationError
              ? 'border-red-500'
              : 'border-gray-700 focus:border-[#8B5CF6]'
          }`}
        />

        {/* Status Icon */}
        <div className="absolute right-3 top-1/2 -translate-y-1/2">
          {isValidating ? (
            <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />
          ) : url && isValid ? (
            <Check className="w-4 h-4 text-green-500" />
          ) : url && validationError ? (
            <X className="w-4 h-4 text-red-500" />
          ) : null}
        </div>
      </div>

      {/* Validation Error */}
      {validationError && (
        <p className="text-xs text-red-400 flex items-center gap-1">
          <X className="w-3 h-3" />
          {validationError}
        </p>
      )}

      {/* Help Text */}
      {!url && (
        <p className="text-xs text-gray-500">
          Enter a YouTube URL to generate clips
        </p>
      )}
    </div>
  );
}

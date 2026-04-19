interface GenerateButtonProps {
  processing: boolean;
  onClick: () => void;
}

export default function GenerateButton({ processing, onClick }: GenerateButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={processing}
      className={`
        w-full py-3 px-6 rounded-lg font-medium text-white transition-all duration-200
        ${processing
          ? 'bg-gray-600 cursor-not-allowed'
          : 'bg-[#8B5CF6] hover:bg-[#7C3AED] active:scale-[0.98]'
        }
      `}
    >
      {processing ? (
        <span className="flex items-center justify-center gap-2">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Processing...
        </span>
      ) : (
        'Generate Clips'
      )}
    </button>
  );
}

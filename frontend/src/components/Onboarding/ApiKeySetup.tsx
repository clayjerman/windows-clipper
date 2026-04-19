import { useState } from 'react';
import { Lock, AlertCircle, CheckCircle, Key, Info } from 'lucide-react';
import { saveApiKeys, loadApiKeys, ApiKeys } from '../../services/settingsStorage';

interface ApiKeySetupProps {
  onComplete: () => void;
}

export default function ApiKeySetup({ onComplete }: ApiKeySetupProps) {
  const [apiKeys, setApiKeys] = useState<ApiKeys>({
    geminiApiKey: loadApiKeys().geminiApiKey,
    openaiApiKey: loadApiKeys().openaiApiKey || ''
  });
  const [showHelp, setShowHelp] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  const handleGeminiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.trim();
    setApiKeys({ ...apiKeys, geminiApiKey: value });
    setError('');
  };

  const handleOpenAIKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.trim();
    setApiKeys({ ...apiKeys, openaiApiKey: value });
  };

  const validateGeminiKey = (key: string): boolean => {
    return key.startsWith('AIza') && key.length >= 30;
  };

  const handleSave = async () => {
    setError('');
    setSaving(true);

    // Validate Gemini key (required)
    if (!apiKeys.geminiApiKey) {
      setError('Gemini API key is required');
      setSaving(false);
      return;
    }

    if (!validateGeminiKey(apiKeys.geminiApiKey)) {
      setError('Invalid Gemini API key format. It should start with "AIza"');
      setSaving(false);
      return;
    }

    try {
      // Save to localStorage
      saveApiKeys(apiKeys);

      // Simulate API verification (optional)
      await new Promise(resolve => setTimeout(resolve, 1000));

      setSaved(true);
      setSaving(false);

      // Wait a moment then proceed
      setTimeout(() => {
        onComplete();
      }, 1500);
    } catch (err) {
      setError('Failed to save API keys. Please try again.');
      setSaving(false);
    }
  };

  const handleSkip = () => {
    // Allow skipping Gemini but warn
    if (!apiKeys.geminiApiKey) {
      const confirmed = window.confirm(
        'Without a Gemini API key, you will not be able to use AI features. ' +
        'You can add it later in settings.\n\nContinue without API key?'
      );
      if (confirmed) {
        saveApiKeys({ geminiApiKey: '', openaiApiKey: apiKeys.openaiApiKey });
        onComplete();
      }
    } else {
      onComplete();
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0C] flex items-center justify-center p-8">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-[#8B5CF6] to-[#EC4899] rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Key className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-3">
            Welcome to AI Clipper
          </h1>
          <p className="text-gray-400 text-lg">
            Setup your API keys to get started
          </p>
        </div>

        {/* API Key Form */}
        <div className="bg-[#1A1A1D] rounded-2xl p-8 shadow-2xl">
          {/* Gemini API Key */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <label className="text-white font-semibold flex items-center gap-2">
                <Lock className="w-4 h-4 text-[#8B5CF6]" />
                Gemini API Key
                <span className="text-red-500 text-xs">*</span>
              </label>
              <button
                onClick={() => setShowHelp(!showHelp)}
                className="text-[#8B5CF6] hover:text-[#A78BFA] text-sm transition-colors"
              >
                {showHelp ? 'Hide' : 'Help'}
              </button>
            </div>

            <input
              type="password"
              value={apiKeys.geminiApiKey}
              onChange={handleGeminiKeyChange}
              placeholder="Enter your Gemini API key"
              className="w-full bg-[#0D0D0F] border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#8B5CF6] transition-colors"
              disabled={saving || saved}
            />

            {showHelp && (
              <div className="mt-3 p-4 bg-[#0D0D0F] rounded-lg">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-[#8B5CF6] mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-gray-400 space-y-2">
                    <p>Get your free Gemini API key:</p>
                    <ol className="list-decimal list-inside space-y-1 text-gray-500">
                      <li>Visit <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-[#8B5CF6] hover:underline">Google AI Studio</a></li>
                      <li>Sign in with your Google account</li>
                      <li>Click "Create API key"</li>
                      <li>Copy and paste the key above</li>
                    </ol>
                    <p className="text-xs text-gray-500">
                      Free tier: 1,500 requests/day. Sufficient for personal use.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {apiKeys.geminiApiKey && validateGeminiKey(apiKeys.geminiApiKey) && (
              <div className="mt-2 flex items-center gap-2 text-green-500 text-sm">
                <CheckCircle className="w-4 h-4" />
                Valid API key format
              </div>
            )}
          </div>

          {/* OpenAI API Key (Optional) */}
          <div className="mb-8">
            <label className="text-white font-semibold flex items-center gap-2 mb-3">
              <Lock className="w-4 h-4 text-gray-500" />
              OpenAI API Key
              <span className="text-gray-500 text-xs">(Optional)</span>
            </label>

            <input
              type="password"
              value={apiKeys.openaiApiKey}
              onChange={handleOpenAIKeyChange}
              placeholder="Enter your OpenAI API key (optional)"
              className="w-full bg-[#0D0D0F] border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-gray-600 transition-colors"
              disabled={saving || saved}
            />

            <p className="mt-2 text-xs text-gray-500">
              Optional: Used for additional AI features. Get it from{' '}
              <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-[#8B5CF6] hover:underline">
                OpenAI Platform
              </a>
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Success Message */}
          {saved && (
            <div className="mb-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
              <p className="text-green-400 text-sm">
                API keys saved successfully! Setting up your workspace...
              </p>
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleSkip}
              disabled={saving || saved}
              className="flex-1 px-6 py-3 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {apiKeys.geminiApiKey ? 'Continue' : 'Skip for Now'}
            </button>

            <button
              onClick={handleSave}
              disabled={saving || saved}
              className="flex-1 px-6 py-3 rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#EC4899] text-white font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Saving...
                </span>
              ) : saved ? (
                <span className="flex items-center justify-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  Saved!
                </span>
              ) : (
                'Save & Continue'
              )}
            </button>
          </div>

          {/* Security Note */}
          <div className="mt-6 pt-6 border-t border-gray-800">
            <p className="text-xs text-gray-500 flex items-start gap-2">
              <Info className="w-3 h-3 flex-shrink-0 mt-0.5" />
              Your API keys are stored securely on your device and are never shared with third parties.
              You can update them anytime in Settings.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-500">
          Need help? Check the{' '}
          <a href="https://github.com/YOUR_USERNAME/ai-clipper/blob/main/docs/FAQ.md" target="_blank" rel="noopener noreferrer" className="text-[#8B5CF6] hover:underline">
            FAQ
          </a>
        </div>
      </div>
    </div>
  );
}

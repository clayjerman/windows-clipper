import { useState, useEffect } from 'react';
import { Settings, Lock, Key, Save, RefreshCw, Info, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import { saveApiKeys, loadApiKeys, clearApiKeys, hasApiKeys } from '../../services/settingsStorage';

export default function SettingsPanel({ onClose }: { onClose: () => void }) {
  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [openaiApiKey, setOpenaiApiKey] = useState('');
  const [showKeys, setShowKeys] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');
  const [hasKeys, setHasKeys] = useState(false);

  useEffect(() => {
    const keys = loadApiKeys();
    setGeminiApiKey(keys.geminiApiKey);
    setOpenaiApiKey(keys.openaiApiKey || '');
    setHasKeys(hasApiKeys());
  }, []);

  const validateGeminiKey = (key: string): boolean => {
    return key.startsWith('AIza') && key.length >= 30;
  };

  const handleSave = async () => {
    setError('');
    setSaving(true);
    setSaved(false);

    try {
      // Validate Gemini key
      if (!geminiApiKey) {
        setError('Gemini API key is required for AI features');
        setSaving(false);
        return;
      }

      if (!validateGeminiKey(geminiApiKey)) {
        setError('Invalid Gemini API key format. It should start with "AIza"');
        setSaving(false);
        return;
      }

      // Save to localStorage
      saveApiKeys({
        geminiApiKey,
        openaiApiKey
      });

      setSaved(true);
      setSaving(false);
      setHasKeys(true);

      // Clear success message after 3 seconds
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError('Failed to save API keys. Please try again.');
      setSaving(false);
    }
  };

  const handleClear = () => {
    const confirmed = window.confirm(
      'Are you sure you want to clear all API keys? You will need to re-enter them to use AI features.'
    );

    if (confirmed) {
      clearApiKeys();
      setGeminiApiKey('');
      setOpenaiApiKey('');
      setHasKeys(false);
      setError('');
    }
  };

  const handleTestKey = async () => {
    // TODO: Implement actual API key testing
    // This would call the backend to verify the key
    setError('');
    setSaving(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 1000));

      if (validateGeminiKey(geminiApiKey)) {
        setError('API key appears valid!');
        setSaved(true);
      } else {
        setError('Invalid API key format');
      }

      setSaving(false);

      setTimeout(() => {
        setError('');
        setSaved(false);
      }, 3000);
    } catch (err) {
      setError('Failed to test API key');
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-8 z-50">
      <div className="bg-[#1A1A1D] rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="p-6 border-b border-gray-800 flex items-center justify-between sticky top-0 bg-[#1A1A1D] z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[#8B5CF6] rounded-lg flex items-center justify-center">
              <Settings className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-xl font-bold text-white">Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* API Keys Section */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Key className="w-5 h-5 text-[#8B5CF6]" />
              <h3 className="text-lg font-semibold text-white">API Keys</h3>
            </div>

            <div className="space-y-4">
              {/* Gemini API Key */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-white text-sm font-medium">
                    Gemini API Key
                    <span className="text-red-500 ml-1">*</span>
                  </label>
                  {hasKeys && geminiApiKey && (
                    <div className="flex items-center gap-1 text-green-500 text-xs">
                      <CheckCircle className="w-3 h-3" />
                      Configured
                    </div>
                  )}
                </div>

                <div className="relative">
                  <input
                    type={showKeys ? 'text' : 'password'}
                    value={geminiApiKey}
                    onChange={(e) => setGeminiApiKey(e.target.value)}
                    placeholder="Enter your Gemini API key"
                    className="w-full bg-[#0D0D0F] border border-gray-700 rounded-lg px-4 py-3 pr-24 text-white placeholder-gray-500 focus:outline-none focus:border-[#8B5CF6] transition-colors"
                    disabled={saving}
                  />

                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                    <button
                      onClick={() => setShowKeys(!showKeys)}
                      className="p-2 text-gray-400 hover:text-white transition-colors"
                      title={showKeys ? 'Hide' : 'Show'}
                    >
                      <Settings className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {geminiApiKey && validateGeminiKey(geminiApiKey) && (
                  <div className="mt-1 text-xs text-green-500 flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" />
                    Valid API key format
                  </div>
                )}

                {!geminiApiKey && (
                  <p className="mt-2 text-xs text-gray-500">
                    Get your free API key from{' '}
                    <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-[#8B5CF6] hover:underline">
                      Google AI Studio
                    </a>
                  </p>
                )}
              </div>

              {/* OpenAI API Key */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-white text-sm font-medium">
                    OpenAI API Key
                    <span className="text-gray-500 ml-1">(Optional)</span>
                  </label>
                  {openaiApiKey && (
                    <div className="flex items-center gap-1 text-green-500 text-xs">
                      <CheckCircle className="w-3 h-3" />
                      Configured
                    </div>
                  )}
                </div>

                <div className="relative">
                  <input
                    type={showKeys ? 'text' : 'password'}
                    value={openaiApiKey}
                    onChange={(e) => setOpenaiApiKey(e.target.value)}
                    placeholder="Enter your OpenAI API key (optional)"
                    className="w-full bg-[#0D0D0F] border border-gray-700 rounded-lg px-4 py-3 pr-24 text-white placeholder-gray-500 focus:outline-none focus:border-gray-600 transition-colors"
                    disabled={saving}
                  />
                </div>

                <p className="mt-2 text-xs text-gray-500">
                  Optional: For additional AI features. Get it from{' '}
                  <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-[#8B5CF6] hover:underline">
                    OpenAI Platform
                  </a>
                </p>
              </div>

              {/* Help Text */}
              <div className="p-3 bg-[#0D0D0F] rounded-lg flex items-start gap-2">
                <Info className="w-4 h-4 text-[#8B5CF6] flex-shrink-0 mt-0.5" />
                <p className="text-xs text-gray-400">
                  Your API keys are stored securely on your device and are never shared with third parties.
                </p>
              </div>
            </div>
          </div>

          {/* Error/Success Messages */}
          {error && !saved && (
            <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {saved && (
            <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
              <p className="text-green-400 text-sm">
                API keys saved successfully!
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4 border-t border-gray-800">
            <button
              onClick={handleClear}
              className="flex-1 px-4 py-2 rounded-lg border border-red-500/20 text-red-400 hover:bg-red-500/10 transition-colors flex items-center justify-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Clear Keys
            </button>

            <button
              onClick={handleTestKey}
              disabled={saving || !geminiApiKey}
              className="flex-1 px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Testing...
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4" />
                  Test Key
                </>
              )}
            </button>

            <button
              onClick={handleSave}
              disabled={saving}
              className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#EC4899] text-white font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {saving ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

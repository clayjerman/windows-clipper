import { AppSettings, defaultSettings } from '../types/settings';

const SETTINGS_KEY = 'ai-clipper-settings';
const API_KEYS_KEY = 'ai-clipper-api-keys';

export interface ApiKeys {
  geminiApiKey: string;
  openaiApiKey?: string;
}

/**
 * Load application settings from localStorage
 */
export function loadSettings(): AppSettings {
  try {
    const stored = localStorage.getItem(SETTINGS_KEY);
    if (stored) {
      return {
        ...defaultSettings,
        ...JSON.parse(stored)
      };
    }
  } catch (error) {
    console.error('Error loading settings:', error);
  }
  return { ...defaultSettings };
}

/**
 * Save application settings to localStorage
 */
export function saveSettings(settings: AppSettings): void {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Error saving settings:', error);
  }
}

/**
 * Load API keys from localStorage
 */
export function loadApiKeys(): ApiKeys {
  try {
    const stored = localStorage.getItem(API_KEYS_KEY);
    if (stored) {
      const keys = JSON.parse(stored);
      return {
        geminiApiKey: keys.geminiApiKey || '',
        openaiApiKey: keys.openaiApiKey || ''
      };
    }
  } catch (error) {
    console.error('Error loading API keys:', error);
  }
  return {
    geminiApiKey: '',
    openaiApiKey: ''
  };
}

/**
 * Save API keys to localStorage
 */
export function saveApiKeys(keys: ApiKeys): void {
  try {
    localStorage.setItem(API_KEYS_KEY, JSON.stringify(keys));
  } catch (error) {
    console.error('Error saving API keys:', error);
  }
}

/**
 * Check if API keys are configured
 */
export function hasApiKeys(): boolean {
  const keys = loadApiKeys();
  return !!keys.geminiApiKey;
}

/**
 * Clear API keys (for logout/reset)
 */
export function clearApiKeys(): void {
  try {
    localStorage.removeItem(API_KEYS_KEY);
  } catch (error) {
    console.error('Error clearing API keys:', error);
  }
}

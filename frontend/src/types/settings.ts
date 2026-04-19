export interface AppSettings {
  geminiApiKey: string;
  openaiApiKey?: string;
  theme: 'dark' | 'light';
  autoSave: boolean;
  defaultClipDuration: number;
  defaultNumberOfClips: number;
  enableSubtitles: boolean;
  enableJumpCuts: boolean;
}

export const defaultSettings: AppSettings = {
  geminiApiKey: '',
  openaiApiKey: '',
  theme: 'dark',
  autoSave: true,
  defaultClipDuration: 30,
  defaultNumberOfClips: 5,
  enableSubtitles: true,
  enableJumpCuts: true,
};

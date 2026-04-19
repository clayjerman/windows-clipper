export interface VideoInfo {
  id: string;
  title: string;
  duration: number;
  thumbnail: string;
  channel: string;
  upload_date: string;
  description?: string;
}

export interface VideoMetadata extends VideoInfo {
  format?: string;
  width?: number;
  height?: number;
  fps?: number;
}

export interface ClipSettings {
  duration: number;
  count: number;
  subtitle_style: string;
  enable_subtitles: boolean;
  enable_jump_cuts: boolean;
}

export interface GenerateRequest {
  url: string;
  settings: ClipSettings;
}

export interface GenerateResponse {
  job_id: string;
  video_info: VideoMetadata;
  status: string;
}

export interface ProcessingProgress {
  stage: string;
  progress: number;
  message: string;
  details?: Record<string, any>;
  current_clip?: number;
  total_clips?: number;
}

export interface Transcription {
  language: string;
  segments: Array<{
    start: number;
    end: number;
    text: string;
    confidence: number;
  }>;
  full_text: string;
}

export interface SpeakerInfo {
  id: number;
  confidence: number;
  start_time: number;
  end_time: number;
}

export interface Clip {
  id: string;
  video_id: string;
  start_time: number;
  end_time: number;
  duration: number;
  title: string;
  description?: string;
  thumbnail?: string;
  viral_score: number;
  transcription?: Transcription;
  speakers?: SpeakerInfo[];
  subtitles_enabled: boolean;
  jump_cuts_enabled: boolean;
  created_at: string;
  enabled: boolean;
  exported?: boolean;
  export_path?: string;
}

export interface ClipExport {
  clip_id: string;
  format: 'mp4' | 'webm' | 'mov';
  quality: '1080p' | '720p' | '480p';
  subtitles: boolean;
}

export interface ExportResult {
  success: boolean;
  clip_id: string;
  output_path: string;
  file_size: number;
  duration: number;
}

export interface JobStatus {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  current_stage: string;
  created_at: string;
  completed_at?: string;
  error?: string;
}

export interface WebSocketMessage {
  type: 'progress' | 'clip_generated' | 'error' | 'complete' | 'export_complete';
  data?: any;
  message?: string;
  timestamp?: number;
}

export interface ApiError {
  error: string;
  details?: string;
}

export interface CacheInfo {
  videos: number;
  transcriptions: number;
  total_size: number;
  last_cleaned: string;
}

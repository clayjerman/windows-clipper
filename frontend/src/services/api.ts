import {
  VideoInfo,
  VideoMetadata,
  ClipSettings,
  GenerateRequest,
  GenerateResponse,
  ProcessingProgress,
  Clip,
  ClipExport,
  ExportResult,
  JobStatus,
  ApiError,
  CacheInfo,
} from '../types/api';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'API request failed');
    }

    return response.json();
  }

  async getVideoInfo(url: string): Promise<VideoMetadata> {
    return this.request<VideoMetadata>('/video/info', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async generateClips(request: GenerateRequest): Promise<GenerateResponse> {
    return this.request<GenerateResponse>('/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getJobStatus(jobId: string): Promise<JobStatus> {
    return this.request<JobStatus>(`/jobs/${jobId}`);
  }

  async getClips(videoId: string): Promise<Clip[]> {
    return this.request<Clip[]>(`/clips/${videoId}`);
  }

  async exportClip(clipId: string, options: Partial<ClipExport> = {}): Promise<ExportResult> {
    return this.request<ExportResult>(`/clips/${clipId}/export`, {
      method: 'POST',
      body: JSON.stringify(options),
    });
  }

  async exportClips(clipIds: string[], options: Partial<ClipExport> = {}): Promise<ExportResult[]> {
    return this.request<ExportResult[]>('/clips/export', {
      method: 'POST',
      body: JSON.stringify({ clip_ids: clipIds, options }),
    });
  }

  async deleteClip(clipId: string): Promise<void> {
    await this.request(`/clips/${clipId}`, {
      method: 'DELETE',
    });
  }

  async getCacheInfo(): Promise<CacheInfo> {
    return this.request<CacheInfo>('/cache/info');
  }

  async clearCache(): Promise<void> {
    await this.request('/cache/clear', {
      method: 'DELETE',
    });
  }

  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiClient = new ApiClient();

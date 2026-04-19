"""
Data models for video processing
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VideoMetadata(BaseModel):
    """Metadata for a video"""
    video_id: str
    title: str
    author: str
    duration: int  # in seconds
    thumbnail_url: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    file_path: Optional[str] = None


class Video(BaseModel):
    """Complete video object"""
    id: str
    url: str
    metadata: VideoMetadata
    status: str = "pending"  # pending, downloading, processing, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None


class ClipSettings(BaseModel):
    """Settings for clip generation"""

    # ── Timing ──────────────────────────────────────────────────────────────
    clip_duration: int = Field(
        default=30, ge=15, le=60,
        description="Duration of each clip in seconds"
    )
    num_clips: int = Field(
        default=5, ge=1, le=10,
        description="Number of clips to generate"
    )

    # ── Subtitles ────────────────────────────────────────────────────────────
    subtitle_style: str = Field(
        default="modern",
        description="Subtitle style: modern, minimal, bold, pop"
    )
    highlight_keywords: bool = Field(
        default=True,
        description="Highlight keywords in subtitles"
    )

    # ── Visual effects ───────────────────────────────────────────────────────
    zoom_effect: bool = Field(
        default=True,
        description="Dynamic zoom on active speaker"
    )
    color_enhance: bool = Field(
        default=False,
        description="Subtle color enhancement (brightness +3%, contrast +10%, saturation +20%)"
    )
    auto_hooks: bool = Field(
        default=True,
        description="Add auto-hook title card for the first 3 seconds"
    )

    # ── Audio ────────────────────────────────────────────────────────────────
    audio_normalize: bool = Field(
        default=True,
        description="Normalize audio to EBU R128 (-16 LUFS) via loudnorm"
    )
    audio_fade_duration: float = Field(
        default=0.3, ge=0.0, le=2.0,
        description="Audio fade-in / fade-out duration in seconds (0 = disabled)"
    )

    # ── Encoding ─────────────────────────────────────────────────────────────
    output_resolution: int = Field(
        default=1080,
        description="Output height in pixels: 480, 720, 1080"
    )
    crf: int = Field(
        default=23, ge=15, le=35,
        description="CRF quality factor (15 = best, 28 = smallest file)"
    )
    hardware_accel: str = Field(
        default="auto",
        description="Video encoder: auto, cpu, nvidia, intel, vaapi"
    )
    output_format: str = Field(
        default="mp4",
        description="Container format: mp4, webm"
    )

    # ── Speed ────────────────────────────────────────────────────────────────
    speed: float = Field(
        default=1.0, ge=0.5, le=2.0,
        description="Playback speed multiplier (1.0 = normal)"
    )


class ProcessingProgress(BaseModel):
    """Progress update for processing"""
    stage: str  # downloading, transcribing, analyzing, detecting, editing, complete
    progress: int = Field(default=0, ge=0, le=100, description="Progress percentage")
    message: str
    current_clip: Optional[int] = None
    total_clips: Optional[int] = None


class TranscriptionSegment(BaseModel):
    """A single transcription segment"""
    start: float
    end: float
    text: str
    confidence: float = 1.0


class Transcription(BaseModel):
    """Complete transcription with timing"""
    text: str
    segments: List[TranscriptionSegment]
    language: str = "en"
    duration: float


class ViralMoment(BaseModel):
    """A detected viral moment"""
    timestamp: float  # seconds
    score: float  # 0-10
    reason: str
    emotional_intensity: float = 0.0
    keywords: List[str] = []
    context: str = ""
    top_reasons: List[str] = []
    overall_score: float = 0.0

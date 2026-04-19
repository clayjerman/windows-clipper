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
    clip_duration: int = Field(default=30, ge=15, le=60, description="Duration of each clip in seconds")
    num_clips: int = Field(default=5, ge=1, le=10, description="Number of clips to generate")
    subtitle_style: str = Field(default="modern", description="Style of subtitles: modern, minimal, bold")
    auto_hooks: bool = Field(default=True, description="Generate auto hooks for first 3 seconds")
    include_b_roll: bool = Field(default=False, description="Add B-roll footage")
    zoom_effect: bool = Field(default=True, description="Add zoom effects on speakers")
    highlight_keywords: bool = Field(default=True, description="Highlight key words dynamically")


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
    reason: str  # Why this moment is viral
    emotional_intensity: float = 0.0
    keywords: List[str] = []
    context: str = ""

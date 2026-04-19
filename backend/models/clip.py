"""
Data models for clips
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SpeakerInfo(BaseModel):
    """Information about detected speaker"""
    face_id: int
    confidence: float
    bounding_box: List[float]  # [x, y, width, height]
    mouth_active: bool
    speaking_probability: float


class Clip(BaseModel):
    """A generated clip"""
    id: str
    video_id: str
    start_time: float  # seconds
    end_time: float  # seconds
    duration: float
    score: float  # Viral score 0-10
    title: str
    description: str
    thumbnail_path: Optional[str] = None
    video_path: Optional[str] = None
    transcription: Optional[str] = None
    subtitles: Optional[str] = None  # SRT format
    speakers: Optional[List[SpeakerInfo]] = None
    enabled: bool = True  # User can disable clips
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "processing"  # processing, ready, failed


class ClipExport(BaseModel):
    """Export settings for clips"""
    clip_ids: List[str]
    format: str = "mp4"
    quality: str = "high"  # low, medium, high
    include_watermark: bool = False


class ExportResult(BaseModel):
    """Result of export operation"""
    success: bool
    exported_clips: List[str]
    total_size_mb: float
    export_path: str
    errors: Optional[List[str]] = None


class DetectedScene(BaseModel):
    """A detected scene change or important moment"""
    timestamp: float
    type: str  # scene_change, emotional_spike, key_moment
    confidence: float
    description: str

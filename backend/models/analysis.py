"""
Data models for AI analysis
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class EmotionType(str, Enum):
    """Types of emotions detected"""
    EXCITEMENT = "excitement"
    LAUGHTER = "laughter"
    SURPRISE = "surprise"
    ANGER = "anger"
    SADNESS = "sadness"
    FEAR = "fear"
    NEUTRAL = "neutral"


class EmotionalSpike(BaseModel):
    """An emotional spike detected in content"""
    timestamp: float
    emotion: EmotionType
    intensity: float = Field(ge=0.0, le=1.0)
    duration: float
    context: str


class KeywordMatch(BaseModel):
    """A matching viral keyword or phrase"""
    keyword: str
    timestamp: float
    confidence: float
    viral_score: float


class ContentAnalysis(BaseModel):
    """Complete content analysis result"""
    video_id: str
    viral_moments: List[float] = []  # Ranked timestamps
    emotional_spikes: List[EmotionalSpike] = []
    viral_keywords: List[KeywordMatch] = []
    scene_changes: List[float] = []
    summary: str = ""
    key_insights: List[str] = []
    recommended_clips: List[Dict] = []  # {start, end, score, reason}


class ViralScoringCriteria(BaseModel):
    """Criteria for viral moment scoring"""
    emotional_weight: float = 0.30
    keyword_weight: float = 0.25
    speaker_weight: float = 0.20
    pacing_weight: float = 0.15
    scene_weight: float = 0.10


class ViralScoreResult(BaseModel):
    """Result of viral scoring"""
    timestamp: float
    overall_score: float  # 0-10
    breakdown: Dict[str, float]  # Individual criteria scores
    top_reasons: List[str]  # Why this scored high

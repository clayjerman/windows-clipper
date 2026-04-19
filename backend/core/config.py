"""
Configuration management for AI Clipper
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = False

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "data")
    DOWNLOADS_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "data", "downloads")
    PROCESSED_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "data", "processed")
    CACHE_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "data", "cache")
    MODELS_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "data", "models")

    # Video Processing
    DEFAULT_CLIP_DURATION: int = 30  # seconds
    MAX_CLIP_DURATION: int = 60
    MIN_CLIP_DURATION: int = 15
    DEFAULT_NUM_CLIPS: int = 5
    OUTPUT_ASPECT_RATIO: str = "9:16"
    OUTPUT_FORMAT: str = "mp4"

    # AI Models
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large
    WHISPER_DEVICE: str = "cpu"  # cpu, cuda
    GEMINI_MODEL: str = "gemini-pro"

    # Processing
    MAX_CONCURRENT_PROCESSES: int = 2
    VIDEO_QUALITY: str = "720p"  # 480p, 720p, 1080p
    AUDIO_QUALITY: str = "192k"

    # Cache
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 86400  # 24 hours in seconds

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create singleton instance
settings = Settings()

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        settings.DATA_DIR,
        settings.DOWNLOADS_DIR,
        settings.PROCESSED_DIR,
        settings.CACHE_DIR,
        settings.MODELS_DIR
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


ensure_directories()

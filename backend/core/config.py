"""
Configuration management for AI Clipper.
Handles both development (source) and packaged (PyInstaller) environments.
"""
import os
import sys
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


def _app_data_dir() -> Path:
    """
    Return a writable data directory that works in both dev and packaged modes.

    - Packaged (PyInstaller): %APPDATA%/AI Clipper  (Windows)
                               ~/Library/Application Support/AI Clipper  (macOS)
                               ~/.local/share/AI Clipper  (Linux)
    - Development:             <project_root>/data
    """
    if getattr(sys, "frozen", False):
        # Running as a PyInstaller bundle
        if sys.platform == "win32":
            base = Path(os.environ.get("APPDATA", Path.home()))
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        return base / "AI Clipper"
    else:
        # Development: place data/ next to the backend package
        here = Path(__file__).resolve()
        project_root = here.parent.parent.parent  # backend/core/config.py → project root
        return project_root / "data"


_DATA_DIR = _app_data_dir()


class Settings(BaseSettings):
    """Application settings — all paths resolved relative to _DATA_DIR."""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = False

    # Paths (converted to str for legacy code that expects str)
    DATA_DIR: str = str(_DATA_DIR)
    DOWNLOADS_DIR: str = str(_DATA_DIR / "downloads")
    PROCESSED_DIR: str = str(_DATA_DIR / "processed")
    CACHE_DIR: str = str(_DATA_DIR / "cache")
    MODELS_DIR: str = str(_DATA_DIR / "models")

    # Video Processing
    DEFAULT_CLIP_DURATION: int = 30
    MAX_CLIP_DURATION: int = 60
    MIN_CLIP_DURATION: int = 15
    DEFAULT_NUM_CLIPS: int = 5
    OUTPUT_ASPECT_RATIO: str = "9:16"
    OUTPUT_FORMAT: str = "mp4"

    # AI Models
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"
    GEMINI_MODEL: str = "gemini-pro"

    # Processing
    MAX_CONCURRENT_PROCESSES: int = 2
    VIDEO_QUALITY: str = "720p"
    AUDIO_QUALITY: str = "192k"

    # Cache
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 86400  # 24 h

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


def ensure_directories():
    """Create all required data directories."""
    for d in [
        settings.DATA_DIR,
        settings.DOWNLOADS_DIR,
        settings.PROCESSED_DIR,
        settings.CACHE_DIR,
        settings.MODELS_DIR,
    ]:
        Path(d).mkdir(parents=True, exist_ok=True)


ensure_directories()

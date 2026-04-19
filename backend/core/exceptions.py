"""
Custom exceptions for AI Clipper
"""


class AIClipperError(Exception):
    """Base exception for AI Clipper"""
    pass


class DownloadError(AIClipperError):
    """Raised when video download fails"""
    pass


class TranscriptionError(AIClipperError):
    """Raised when transcription fails"""
    pass


class AnalysisError(AIClipperError):
    """Raised when AI analysis fails"""
    pass


class VideoProcessingError(AIClipperError):
    """Raised when video processing fails"""
    pass


class InvalidURLError(AIClipperError):
    """Raised when URL is invalid"""
    pass


class FileNotFound(AIClipperError):
    """Raised when required file is not found"""
    pass


class ConfigurationError(AIClipperError):
    """Raised when configuration is invalid"""
    pass

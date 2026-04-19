"""
YouTube video downloader using yt-dlp
"""
import os
import logging
from typing import Optional, Dict
from pathlib import Path
from yt_dlp import YoutubeDL
from datetime import datetime

from ..core.config import settings
from ..core.exceptions import DownloadError, InvalidURLError
from ..models.video import VideoMetadata, Video

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Download videos from YouTube using yt-dlp"""

    def __init__(self):
        self.download_dir = settings.DOWNLOADS_DIR

    def validate_url(self, url: str) -> bool:
        """
        Validate if URL is a valid YouTube URL

        Args:
            url: YouTube URL to validate

        Returns:
            True if valid, False otherwise
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info is not None
        except Exception as e:
            logger.warning(f"URL validation failed: {e}")
            return False

    def get_video_info(self, url: str) -> VideoMetadata:
        """
        Get video metadata without downloading

        Args:
            url: YouTube URL

        Returns:
            VideoMetadata object

        Raises:
            InvalidURLError: If URL is invalid
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if not info:
                    raise InvalidURLError(f"Could not extract info from URL: {url}")

                metadata = VideoMetadata(
                    video_id=info.get('id', ''),
                    title=info.get('title', 'Unknown'),
                    author=info.get('channel', 'Unknown'),
                    duration=info.get('duration', 0),
                    thumbnail_url=info.get('thumbnail'),
                    upload_date=info.get('upload_date'),
                    view_count=info.get('view_count')
                )

                logger.info(f"Retrieved metadata for: {metadata.title}")
                return metadata

        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise InvalidURLError(f"Failed to get video info: {str(e)}")

    def download(self, url: str, quality: str = "720p", progress_callback=None) -> str:
        """
        Download video from YouTube

        Args:
            url: YouTube URL
            quality: Video quality (480p, 720p, 1080p)
            progress_callback: Optional callback function for progress updates

        Returns:
            Path to downloaded video file

        Raises:
            DownloadError: If download fails
        """
        if not self.validate_url(url):
            raise InvalidURLError(f"Invalid YouTube URL: {url}")

        # Quality settings
        quality_map = {
            "480p": "worst[height<=480][ext=mp4]/worst[ext=mp4]/worst",
            "720p": "best[height<=720][ext=mp4]/best[ext=mp4]/best",
            "1080p": "best[height<=1080][ext=mp4]/best[ext=mp4]/best"
        }

        format_selector = quality_map.get(quality, quality_map["720p"])

        # Generate filename
        video_info = self.get_video_info(url)
        safe_title = "".join(c for c in video_info.title if c.isalnum() or c in (' ', '-', '_')).strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{video_info.video_id}_{timestamp}.mp4"
        output_path = os.path.join(self.download_dir, filename)

        # Check if already downloaded
        if os.path.exists(output_path):
            logger.info(f"Video already downloaded: {output_path}")
            return output_path

        # yt-dlp options
        ydl_opts = {
            'format': format_selector,
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [progress_callback] if progress_callback else [],
        }

        try:
            logger.info(f"Starting download: {url}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if not os.path.exists(output_path):
                raise DownloadError(f"Download completed but file not found: {output_path}")

            logger.info(f"Successfully downloaded to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise DownloadError(f"Failed to download video: {str(e)}")

    def download_audio_only(self, url: str, progress_callback=None) -> str:
        """
        Download only audio from YouTube (for transcription)

        Args:
            url: YouTube URL
            progress_callback: Optional callback for progress updates

        Returns:
            Path to downloaded audio file
        """
        if not self.validate_url(url):
            raise InvalidURLError(f"Invalid YouTube URL: {url}")

        video_info = self.get_video_info(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{video_info.video_id}_{timestamp}_audio.mp3"
        output_path = os.path.join(self.download_dir, filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'progress_hooks': [progress_callback] if progress_callback else [],
        }

        try:
            logger.info(f"Downloading audio: {url}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            logger.info(f"Audio downloaded to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Audio download failed: {e}")
            raise DownloadError(f"Failed to download audio: {str(e)}")

    def cleanup_old_downloads(self, days_old: int = 7):
        """
        Clean up downloaded videos older than specified days

        Args:
            days_old: Age in days
        """
        import time

        now = time.time()
        cutoff = now - (days_old * 86400)  # Convert to seconds

        deleted_count = 0
        freed_space = 0

        for filename in os.listdir(self.download_dir):
            filepath = os.path.join(self.download_dir, filename)
            if os.path.isfile(filepath):
                file_mtime = os.path.getmtime(filepath)
                if file_mtime < cutoff:
                    file_size = os.path.getsize(filepath)
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                        freed_space += file_size
                        logger.info(f"Deleted old file: {filename}")
                    except Exception as e:
                        logger.warning(f"Failed to delete {filename}: {e}")

        logger.info(f"Cleanup complete: Deleted {deleted_count} files, freed {freed_space / (1024**2):.2f} MB")

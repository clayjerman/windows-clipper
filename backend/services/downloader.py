"""
YouTube video downloader — yt-dlp with async progress reporting,
download-cache (skip re-download for same video ID), and pathlib throughout.
"""
import asyncio
import logging
import time
from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional

from yt_dlp import YoutubeDL

from ..core.config import settings
from ..core.exceptions import DownloadError, InvalidURLError
from ..models.video import VideoMetadata

logger = logging.getLogger(__name__)

# Quality → yt-dlp format selector
_QUALITY_MAP = {
    "480p":  "best[height<=480][ext=mp4]/best[height<=480]/bestvideo[height<=480]+bestaudio/best",
    "720p":  "best[height<=720][ext=mp4]/best[height<=720]/bestvideo[height<=720]+bestaudio/best",
    "1080p": "best[height<=1080][ext=mp4]/best[height<=1080]/bestvideo[height<=1080]+bestaudio/best",
}


class VideoDownloader:
    """Download videos from YouTube using yt-dlp."""

    def __init__(self):
        self.download_dir = Path(settings.DOWNLOADS_DIR)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    # ── Metadata ──────────────────────────────────────────────────────────────

    @lru_cache(maxsize=64)
    def get_video_info(self, url: str) -> VideoMetadata:
        """
        Fetch video metadata without downloading.
        Results are in-process cached via lru_cache to avoid duplicate API calls.
        """
        opts = {"quiet": True, "no_warnings": True}
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise InvalidURLError(f"No info for URL: {url}")
                return VideoMetadata(
                    video_id=info.get("id", ""),
                    title=info.get("title", "Unknown"),
                    author=info.get("channel") or info.get("uploader", "Unknown"),
                    duration=int(info.get("duration") or 0),
                    thumbnail_url=info.get("thumbnail"),
                    upload_date=info.get("upload_date"),
                    view_count=info.get("view_count"),
                )
        except InvalidURLError:
            raise
        except Exception as exc:
            raise InvalidURLError(f"Failed to fetch video info: {exc}") from exc

    def validate_url(self, url: str) -> bool:
        try:
            self.get_video_info(url)
            return True
        except InvalidURLError:
            return False

    # ── Download ──────────────────────────────────────────────────────────────

    def download(
        self,
        url: str,
        quality: str = "720p",
        progress_callback: Optional[Callable[[str, int], None]] = None,
    ) -> str:
        """
        Download video to disk and return the local file path.

        Args:
            url: YouTube URL
            quality: "480p" | "720p" | "1080p"
            progress_callback: optional fn(message: str, percent: int)

        Returns:
            Absolute path to the downloaded MP4 file.
        """
        metadata = self.get_video_info(url)

        # Check cache — skip download if same video_id already exists
        existing = self._find_cached(metadata.video_id)
        if existing:
            logger.info(f"Cache hit: {existing}")
            if progress_callback:
                progress_callback("Using cached download", 100)
            return existing

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{metadata.video_id}_{timestamp}.mp4"
        output_path = str(self.download_dir / filename)

        format_selector = _QUALITY_MAP.get(quality, _QUALITY_MAP["720p"])

        last_reported = [-1]  # mutable cell for closure

        def _on_progress(d: dict):
            if progress_callback and d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                if total > 0:
                    pct = int(downloaded * 100 / total)
                    if pct != last_reported[0]:
                        last_reported[0] = pct
                        mb_done = downloaded / 1_048_576
                        mb_total = total / 1_048_576
                        progress_callback(
                            f"Downloading… {mb_done:.1f} / {mb_total:.1f} MB",
                            pct,
                        )
            elif progress_callback and d.get("status") == "finished":
                progress_callback("Download finished, processing…", 100)

        opts: dict = {
            "format": format_selector,
            "outtmpl": output_path,
            "quiet": False,
            "no_warnings": False,
            "progress_hooks": [_on_progress],
            # Merge audio+video when separate streams are fetched
            "merge_output_format": "mp4",
            # Retry settings for reliability
            "retries": 3,
            "fragment_retries": 3,
            "concurrent_fragment_downloads": 4,
        }

        try:
            logger.info(f"Downloading: {url} ({quality})")
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as exc:
            raise DownloadError(f"Download failed: {exc}") from exc

        # yt-dlp may suffix the extension — resolve to the actual file
        actual = self._resolve_output(output_path)
        if not actual:
            raise DownloadError(f"Download finished but file not found: {output_path}")

        logger.info(f"Downloaded: {actual}")
        return actual

    async def download_async(
        self,
        url: str,
        quality: str = "720p",
        progress_callback: Optional[Callable[[str, int], None]] = None,
    ) -> str:
        """
        Async wrapper: runs the blocking download in a thread-pool so the
        FastAPI event loop stays responsive and WebSocket messages keep flowing.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.download(url, quality, progress_callback),
        )

    def download_audio_only(self, url: str) -> str:
        """Download audio-only MP3 (used for transcription fallback)."""
        metadata = self.get_video_info(url)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{metadata.video_id}_{timestamp}_audio.mp3"
        output_path = str(self.download_dir / filename)

        opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": False,
        }
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as exc:
            raise DownloadError(f"Audio download failed: {exc}") from exc

        actual = self._resolve_output(output_path)
        if not actual:
            raise DownloadError(f"Audio file not found after download: {output_path}")
        return actual

    # ── Housekeeping ─────────────────────────────────────────────────────────

    def cleanup_old_downloads(self, days_old: int = 7):
        """Delete download files older than `days_old` days."""
        cutoff = time.time() - days_old * 86_400
        deleted, freed = 0, 0
        for fp in self.download_dir.iterdir():
            if fp.is_file() and fp.stat().st_mtime < cutoff:
                size = fp.stat().st_size
                try:
                    fp.unlink()
                    deleted += 1
                    freed += size
                    logger.info(f"Deleted old file: {fp.name}")
                except OSError as exc:
                    logger.warning(f"Could not delete {fp.name}: {exc}")
        logger.info(
            f"Cleanup done: {deleted} file(s) deleted, "
            f"{freed / 1_048_576:.1f} MB freed"
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _find_cached(self, video_id: str) -> Optional[str]:
        """Return path of an existing download for this video_id, or None."""
        for fp in self.download_dir.glob(f"{video_id}_*.mp4"):
            if fp.is_file():
                return str(fp)
        return None

    def _resolve_output(self, expected_path: str) -> Optional[str]:
        """
        yt-dlp may change the extension or add a suffix.
        Try the expected path first, then glob for the stem.
        """
        ep = Path(expected_path)
        if ep.exists():
            return str(ep)
        # Search for any file with the same stem in the same directory
        for fp in ep.parent.glob(f"{ep.stem}*"):
            if fp.is_file():
                return str(fp)
        return None

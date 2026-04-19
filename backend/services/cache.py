"""
Local caching service for transcriptions and analyses
"""
import os
import json
import logging
import hashlib
from typing import Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from ..core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Cache service for storing processed data"""

    def __init__(self):
        """Initialize cache service"""
        self.cache_dir = settings.CACHE_DIR
        self.ttl = settings.CACHE_TTL
        self.enabled = settings.ENABLE_CACHE

        os.makedirs(self.cache_dir, exist_ok=True)
        logger.info("Cache service initialized")

    def _get_cache_key(self, *args) -> str:
        """
        Generate cache key from arguments

        Args:
            *args: Arguments to hash

        Returns:
            Cache key string
        """
        key_string = "_".join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> str:
        """Get full path for cache file"""
        return os.path.join(self.cache_dir, f"{key}.json")

    def _is_expired(self, cache_path: str) -> bool:
        """Check if cache entry has expired"""
        try:
            mtime = os.path.getmtime(cache_path)
            age = datetime.now().timestamp() - mtime
            return age > self.ttl
        except OSError:
            return True

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if not self.enabled:
            return None

        cache_path = self._get_cache_path(key)

        if not os.path.exists(cache_path):
            return None

        if self._is_expired(cache_path):
            logger.debug(f"Cache expired: {key}")
            try:
                os.remove(cache_path)
            except OSError:
                pass
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f"Cache hit: {key}")
            return data
        except Exception as e:
            logger.warning(f"Failed to read cache: {e}")
            return None

    def set(self, key: str, value: Any) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache

        Returns:
            True if successful
        """
        if not self.enabled:
            return False

        cache_path = self._get_cache_path(key)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(value, f, indent=2, ensure_ascii=False, default=str)
            logger.debug(f"Cache set: {key}")
            return True
        except Exception as e:
            logger.warning(f"Failed to write cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete cache entry

        Args:
            key: Cache key

        Returns:
            True if deleted
        """
        cache_path = self._get_cache_path(key)

        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
                logger.debug(f"Cache deleted: {key}")
                return True
            except OSError as e:
                logger.warning(f"Failed to delete cache: {e}")
                return False

        return False

    def clear_all(self) -> int:
        """
        Clear all cache entries

        Returns:
            Number of entries cleared
        """
        count = 0

        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    os.remove(filepath)
                    count += 1

            logger.info(f"Cleared {count} cache entries")
            return count

        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return 0

    def get_video_transcription(self, video_id: str) -> Optional[dict]:
        """Get cached transcription for video"""
        key = self._get_cache_key("transcription", video_id)
        return self.get(key)

    def set_video_transcription(self, video_id: str, transcription: dict) -> bool:
        """Cache transcription for video"""
        key = self._get_cache_key("transcription", video_id)
        return self.set(key, transcription)

    def get_video_analysis(self, video_id: str) -> Optional[dict]:
        """Get cached analysis for video"""
        key = self._get_cache_key("analysis", video_id)
        return self.get(key)

    def set_video_analysis(self, video_id: str, analysis: dict) -> bool:
        """Cache analysis for video"""
        key = self._get_cache_key("analysis", video_id)
        return self.set(key, analysis)

    def get_video_metadata(self, video_id: str) -> Optional[dict]:
        """Get cached metadata for video"""
        key = self._get_cache_key("metadata", video_id)
        return self.get(key)

    def set_video_metadata(self, video_id: str, metadata: dict) -> bool:
        """Cache metadata for video"""
        key = self._get_cache_key("metadata", video_id)
        return self.set(key, metadata)

    def cleanup_expired(self) -> int:
        """
        Clean up all expired cache entries

        Returns:
            Number of entries cleaned up
        """
        count = 0

        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)

                    if self._is_expired(filepath):
                        os.remove(filepath)
                        count += 1

            logger.info(f"Cleaned up {count} expired cache entries")
            return count

        except Exception as e:
            logger.error(f"Failed to cleanup cache: {e}")
            return 0

    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        stats = {
            "total_entries": 0,
            "total_size_bytes": 0,
            "expired_entries": 0
        }

        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    stats["total_entries"] += 1
                    stats["total_size_bytes"] += os.path.getsize(filepath)

                    if self._is_expired(filepath):
                        stats["expired_entries"] += 1

        except Exception as e:
            logger.warning(f"Failed to get cache stats: {e}")

        stats["total_size_mb"] = round(stats["total_size_bytes"] / (1024 * 1024), 2)
        return stats

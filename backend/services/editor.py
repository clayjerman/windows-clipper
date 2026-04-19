"""
Video editing service using FFmpeg
"""
import os
import logging
import subprocess
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import cv2
import numpy as np

from ..core.config import settings
from ..core.exceptions import VideoProcessingError
from ..models.video import Transcription, TranscriptionSegment
from ..models.clip import Clip, SpeakerInfo

logger = logging.getLogger(__name__)


class VideoEditor:
    """Edit videos using FFmpeg"""

    def __init__(self):
        """Initialize video editor"""
        self.output_dir = settings.PROCESSED_DIR

        # Verify FFmpeg is available
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Verify FFmpeg is installed and accessible"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("FFmpeg detected and accessible")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise VideoProcessingError(
                "FFmpeg not found. Please install FFmpeg and add it to your PATH."
            )

    def cut_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: str = None
    ) -> str:
        """
        Cut a clip from video

        Args:
            video_path: Path to source video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Path for output (auto-generated if None)

        Returns:
            Path to output clip
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_{start_time:.0f}-{end_time:.0f}.mp4"
            )

        duration = end_time - start_time

        try:
            logger.info(f"Cutting clip: {start_time:.2f}s - {end_time:.2f}s")

            # FFmpeg command for cutting
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-avoid_negative_ts', '1',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            if not os.path.exists(output_path):
                raise VideoProcessingError(f"Clip not created: {output_path}")

            logger.info(f"Clip created: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to cut clip: {e}")
            raise VideoProcessingError(f"Failed to cut clip: {str(e)}")

    def convert_to_vertical(
        self,
        video_path: str,
        output_path: str = None,
        crop_strategy: str = "center"
    ) -> str:
        """
        Convert video to vertical format (9:16)

        Args:
            video_path: Path to source video
            output_path: Path for output
            crop_strategy: How to crop ("center", "smart")

        Returns:
            Path to vertical video
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_vertical.mp4"
            )

        try:
            # Get video dimensions
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()

            # Calculate vertical crop dimensions
            # For 9:16 ratio: if original is 16:9, crop center to 9:16
            target_width = int(height * 9 / 16)
            x_offset = (width - target_width) // 2

            logger.info(f"Converting to vertical: {width}x{height} -> {target_width}x{height}")

            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'crop={target_width}:{height}:{x_offset}:0',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            logger.info(f"Vertical video created: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to convert to vertical: {e}")
            raise VideoProcessingError(f"Failed to convert to vertical: {str(e)}")

    def smart_crop_to_speaker(
        self,
        video_path: str,
        speaker_tracking: List[Tuple[int, SpeakerInfo]],
        output_path: str = None
    ) -> str:
        """
        Smart crop video to follow active speaker

        Args:
            video_path: Path to source video
            speaker_tracking: List of (frame_idx, SpeakerInfo)
            output_path: Path for output

        Returns:
            Path to cropped video
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_smart_crop.mp4"
            )

        try:
            # Get video info
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()

            logger.info(f"Smart cropping: {total_frames} frames at {fps} FPS")

            # Create FFmpeg filter complex for dynamic cropping
            # This is simplified - full implementation would use FFmpeg's zoompan filter
            target_width = int(height * 9 / 16)

            # For MVP, use center crop (full implementation would use dynamic crop)
            x_offset = (width - target_width) // 2

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'crop={target_width}:{height}:{x_offset}:0',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            logger.info(f"Smart crop complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to smart crop: {e}")
            raise VideoProcessingError(f"Failed to smart crop: {str(e)}")

    def add_subtitles(
        self,
        video_path: str,
        transcription: Transcription,
        output_path: str = None,
        style: str = "modern"
    ) -> str:
        """
        Add subtitles to video

        Args:
            video_path: Path to source video
            transcription: Transcription with segments
            output_path: Path for output
            style: Subtitle style ("modern", "minimal", "bold")

        Returns:
            Path to video with subtitles
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_subtitled.mp4"
            )

        # Generate ASS subtitle file
        ass_path = output_path.replace('.mp4', '.ass')
        self._generate_ass_subtitles(transcription, ass_path, style)

        try:
            logger.info(f"Adding subtitles with style: {style}")

            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'ass={ass_path}',
                '-c:a', 'copy',
                '-preset', 'fast',
                '-crf', '23',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            # Clean up ASS file
            if os.path.exists(ass_path):
                os.remove(ass_path)

            logger.info(f"Subtitles added: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to add subtitles: {e}")
            raise VideoProcessingError(f"Failed to add subtitles: {str(e)}")

    def _generate_ass_subtitles(
        self,
        transcription: Transcription,
        output_path: str,
        style: str
    ):
        """Generate ASS subtitle file"""
        styles = {
            "modern": "Fontname=Arial, Fontsize=48, PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000, BackColour=&H80000000, Bold=1, Alignment=2",
            "minimal": "Fontname=Helvetica, Fontsize=42, PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000, BackColour=&H80000000, Bold=0, Alignment=2",
            "bold": "Fontname=Impact, Fontsize=52, PrimaryColour=&H00FFFFFF, OutlineColour=&H00000000, BackColour=&H80000000, Bold=1, Alignment=2"
        }

        style_def = styles.get(style, styles["modern"])

        ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style_def}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        for segment in transcription.segments:
            start_time = self._format_ass_time(segment.start)
            end_time = self._format_ass_time(segment.end)
            text = segment.text.replace('\n', ' ')

            ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)

    def _format_ass_time(self, seconds: float) -> str:
        """Format seconds to ASS timestamp (H:MM:SS.mm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{millis:02d}"

    def generate_thumbnail(
        self,
        video_path: str,
        timestamp: float,
        output_path: str = None
    ) -> str:
        """
        Generate thumbnail at timestamp

        Args:
            video_path: Path to video
            timestamp: Timestamp in seconds
            output_path: Path for thumbnail

        Returns:
            Path to thumbnail image
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_thumb_{timestamp:.0f}.jpg"
            )

        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(timestamp),
                '-vframes', '1',
                '-q:v', '2',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            logger.info(f"Thumbnail generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate thumbnail: {e}")
            raise VideoProcessingError(f"Failed to generate thumbnail: {str(e)}")

    def add_zoom_effect(
        self,
        video_path: str,
        speaker_tracking: List[Tuple[int, SpeakerInfo]],
        output_path: str = None
    ) -> str:
        """
        Add dynamic zoom effect focusing on speaker

        Args:
            video_path: Path to source video
            speaker_tracking: Speaker tracking data
            output_path: Path for output

        Returns:
            Path to video with zoom effect
        """
        if output_path is None:
            video_id = Path(video_path).stem
            output_path = os.path.join(
                self.output_dir,
                f"{video_id}_zoom.mp4"
            )

        try:
            # Get video info
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            logger.info(f"Adding zoom effect to {total_frames} frames")

            # For MVP, use simple zoom-in effect
            # Full implementation would use speaker tracking for dynamic zoom
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', 'zoompan=z=1.2:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                '-crf', '23',
                '-shortest',
                '-y', output_path
            ]

            subprocess.run(cmd, check=True, capture_output=True)

            logger.info(f"Zoom effect added: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to add zoom effect: {e}")
            raise VideoProcessingError(f"Failed to add zoom effect: {str(e)}")

    def process_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        add_subtitles: bool = True,
        transcription: Transcription = None,
        add_zoom: bool = False,
        subtitle_style: str = "modern"
    ) -> str:
        """
        Process a complete clip with all enhancements

        Args:
            video_path: Path to source video
            start_time: Start time
            end_time: End time
            add_subtitles: Whether to add subtitles
            transcription: Transcription for subtitles
            add_zoom: Whether to add zoom effect
            subtitle_style: Style of subtitles

        Returns:
            Path to final processed clip
        """
        video_id = Path(video_path).stem
        temp_clip = os.path.join(self.output_dir, f"temp_{video_id}.mp4")

        try:
            # Step 1: Cut clip
            logger.info(f"Processing clip: {start_time:.2f}s - {end_time:.2f}s")
            clip_path = self.cut_clip(video_path, start_time, end_time, temp_clip)

            # Step 2: Convert to vertical
            vertical_path = self.convert_to_vertical(clip_path)
            os.remove(clip_path)

            current_path = vertical_path

            # Step 3: Add zoom effect
            if add_zoom:
                zoom_path = os.path.join(self.output_dir, f"zoom_{video_id}.mp4")
                current_path = self.add_zoom_effect(current_path, [], zoom_path)
                os.remove(vertical_path)

            # Step 4: Add subtitles
            if add_subtitles and transcription:
                final_path = os.path.join(
                    self.output_dir,
                    f"{video_id}_{start_time:.0f}-{end_time:.0f}_final.mp4"
                )
                current_path = self.add_subtitles(current_path, transcription, final_path, subtitle_style)
            else:
                final_path = current_path

            logger.info(f"Clip processing complete: {final_path}")
            return final_path

        except Exception as e:
            logger.error(f"Failed to process clip: {e}")
            raise VideoProcessingError(f"Failed to process clip: {str(e)}")

"""
Transcription service using OpenAI Whisper
"""
import os
import logging
import torch
import whisper
from typing import Optional, List
from pathlib import Path
import json

from ..core.config import settings
from ..core.exceptions import TranscriptionError
from ..models.video import Transcription, TranscriptionSegment

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribe audio using Whisper"""

    def __init__(self, model_size: str = None):
        """
        Initialize transcriber with specified model

        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size or settings.WHISPER_MODEL
        self.device = settings.WHISPER_DEVICE
        self.model = None
        self._model_loaded = False

    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self._model_loaded:
            return

        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(
                self.model_size,
                device=self.device
            )
            self._model_loaded = True
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise TranscriptionError(f"Failed to load transcription model: {str(e)}")

    def transcribe(
        self,
        audio_path: str,
        language: str = "en",
        progress_callback=None
    ) -> Transcription:
        """
        Transcribe audio file

        Args:
            audio_path: Path to audio file
            language: Language code (default: 'en')
            progress_callback: Optional callback for progress updates

        Returns:
            Transcription object with text and segments
        """
        if not os.path.exists(audio_path):
            raise TranscriptionError(f"Audio file not found: {audio_path}")

        self.load_model()

        try:
            logger.info(f"Transcribing: {audio_path}")

            if progress_callback:
                progress_callback(10, "Starting transcription...")

            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                fp16=torch.cuda.is_available() if self.device == "cuda" else False,
                word_timestamps=True
            )

            if progress_callback:
                progress_callback(90, "Processing transcription...")

            # Convert segments
            segments = []
            for seg in result['segments']:
                segments.append(TranscriptionSegment(
                    start=seg['start'],
                    end=seg['end'],
                    text=seg['text'].strip(),
                    confidence=seg.get('no_speech_prob', 1.0)
                ))

            transcription = Transcription(
                text=result['text'],
                segments=segments,
                language=result.get('language', language),
                duration=result.get('duration', 0)
            )

            logger.info(f"Transcription complete: {len(segments)} segments, {transcription.duration:.2f}s")

            if progress_callback:
                progress_callback(100, "Transcription complete")

            return transcription

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(f"Failed to transcribe audio: {str(e)}")

    def transcribe_video(self, video_path: str, **kwargs) -> Transcription:
        """
        Transcribe video file (extracts audio first)

        Args:
            video_path: Path to video file
            **kwargs: Additional arguments for transcribe()

        Returns:
            Transcription object
        """
        # Extract audio using ffmpeg
        import subprocess

        audio_path = video_path.rsplit('.', 1)[0] + '_temp.wav'

        try:
            # Extract audio
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1',
                '-y', audio_path
            ]

            logger.info(f"Extracting audio from video...")
            subprocess.run(cmd, check=True, capture_output=True)

            # Transcribe
            transcription = self.transcribe(audio_path, **kwargs)

            # Clean up temp file
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return transcription

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract audio: {e}")
            raise TranscriptionError(f"Failed to extract audio from video: {str(e)}")
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(str(e))

    def generate_srt(self, transcription: Transcription) -> str:
        """
        Generate SRT subtitle file from transcription

        Args:
            transcription: Transcription object

        Returns:
            SRT formatted string
        """
        srt_lines = []

        for i, segment in enumerate(transcription.segments, 1):
            start_time = self._format_timestamp(segment.start)
            end_time = self._format_timestamp(segment.end)

            srt_lines.append(str(i))
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.append(segment.text)
            srt_lines.append("")  # Empty line between segments

        return "\n".join(srt_lines)

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds to SRT timestamp format (00:00:00,000)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def save_transcription(self, transcription: Transcription, output_path: str):
        """
        Save transcription to JSON file

        Args:
            transcription: Transcription object
            output_path: Path to save JSON
        """
        try:
            data = {
                'text': transcription.text,
                'language': transcription.language,
                'duration': transcription.duration,
                'segments': [
                    {
                        'start': seg.start,
                        'end': seg.end,
                        'text': seg.text,
                        'confidence': seg.confidence
                    }
                    for seg in transcription.segments
                ]
            }

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Transcription saved to: {output_path}")

        except Exception as e:
            logger.error(f"Failed to save transcription: {e}")
            raise

    def load_transcription(self, input_path: str) -> Transcription:
        """
        Load transcription from JSON file

        Args:
            input_path: Path to JSON file

        Returns:
            Transcription object
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            segments = [
                TranscriptionSegment(**seg)
                for seg in data.get('segments', [])
            ]

            return Transcription(
                text=data.get('text', ''),
                segments=segments,
                language=data.get('language', 'en'),
                duration=data.get('duration', 0)
            )

        except Exception as e:
            logger.error(f"Failed to load transcription: {e}")
            raise TranscriptionError(f"Failed to load transcription: {str(e)}")

"""
Video editing service using FFmpeg — single-pass filter chains,
hardware-acceleration fallback, audio normalisation, colour grading.
"""
import os
import json
import logging
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Tuple

from ..core.config import settings
from ..core.exceptions import VideoProcessingError
from ..models.video import ClipSettings, Transcription, TranscriptionSegment
from ..models.clip import Clip, SpeakerInfo

logger = logging.getLogger(__name__)

# Resolution presets: height → (width, height) for 9:16
_RESOLUTION_MAP = {
    480:  (270,  480),
    720:  (405,  720),
    1080: (607, 1080),   # nearest-even 9:16 at 1080p
}


# ─── Hardware-encoder probe ──────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _detect_hw_encoder() -> str:
    """
    Detect the fastest available H.264 hardware encoder.
    Returns one of: h264_nvenc, h264_qsv, h264_vaapi, libx264
    """
    candidates = [
        ("h264_nvenc",  ["-f", "lavfi", "-i", "color=black:s=64x64:d=1",
                         "-c:v", "h264_nvenc", "-f", "null", "-"]),
        ("h264_qsv",    ["-f", "lavfi", "-i", "color=black:s=64x64:d=1",
                         "-c:v", "h264_qsv",  "-f", "null", "-"]),
        ("h264_vaapi",  ["-vaapi_device", "/dev/dri/renderD128",
                         "-f", "lavfi", "-i", "color=black:s=64x64:d=1",
                         "-vf", "format=nv12,hwupload",
                         "-c:v", "h264_vaapi", "-f", "null", "-"]),
    ]
    for name, extra_args in candidates:
        try:
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error"] + extra_args,
                capture_output=True, timeout=5, check=True,
            )
            logger.info(f"Hardware encoder available: {name}")
            return name
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            continue
    logger.info("No hardware encoder found, using libx264")
    return "libx264"


def _choose_encoder(preference: str) -> str:
    """Resolve the encoder string from settings, with auto-detect."""
    if preference == "auto":
        return _detect_hw_encoder()
    mapping = {
        "nvidia": "h264_nvenc",
        "intel":  "h264_qsv",
        "vaapi":  "h264_vaapi",
        "cpu":    "libx264",
    }
    return mapping.get(preference, "libx264")


def _encoder_quality_flag(encoder: str, crf: int) -> List[str]:
    """Return the quality flags for the chosen encoder."""
    if encoder == "h264_nvenc":
        return ["-cq", str(crf), "-preset", "p4"]
    if encoder == "h264_qsv":
        return ["-global_quality", str(crf)]
    if encoder == "h264_vaapi":
        return ["-qp", str(crf)]
    # libx264 / libx265 default
    return ["-crf", str(crf), "-preset", "fast"]


# ─── ASS subtitle generation ─────────────────────────────────────────────────

_SUBTITLE_STYLES = {
    "modern": (
        "Fontname=Arial,Fontsize=52,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BackColour=&H80000000,"
        "Bold=1,Italic=0,Outline=2,Shadow=1,Alignment=2,"
        "MarginL=20,MarginR=20,MarginV=40"
    ),
    "minimal": (
        "Fontname=Helvetica Neue,Fontsize=44,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BackColour=&H60000000,"
        "Bold=0,Italic=0,Outline=1,Shadow=0,Alignment=2,"
        "MarginL=20,MarginR=20,MarginV=40"
    ),
    "bold": (
        "Fontname=Impact,Fontsize=58,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BackColour=&H00000000,"
        "Bold=1,Italic=0,Outline=3,Shadow=2,Alignment=2,"
        "MarginL=20,MarginR=20,MarginV=40"
    ),
    "pop": (
        "Fontname=Arial Rounded MT Bold,Fontsize=56,PrimaryColour=&H00FFFF00,"
        "OutlineColour=&H00000000,BackColour=&H00000000,"
        "Bold=1,Italic=0,Outline=3,Shadow=2,Alignment=2,"
        "MarginL=20,MarginR=20,MarginV=40"
    ),
}


def _format_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _generate_ass(transcription: Transcription, output_path: str, style: str = "modern"):
    style_def = _SUBTITLE_STYLES.get(style, _SUBTITLE_STYLES["modern"])
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
        "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{style_def}",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for seg in transcription.segments:
        text = seg.text.strip().replace("\n", " ")
        lines.append(
            f"Dialogue: 0,{_format_ass_time(seg.start)},"
            f"{_format_ass_time(seg.end)},Default,,0,0,0,,{text}"
        )
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


# ─── VideoEditor ─────────────────────────────────────────────────────────────

class VideoEditor:
    """Edit videos using FFmpeg with single-pass filter chains."""

    def __init__(self):
        self.output_dir = Path(settings.PROCESSED_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True, check=True,
            )
            logger.info("FFmpeg detected")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise VideoProcessingError(
                "FFmpeg not found. Install FFmpeg and add it to PATH."
            )

    # ── Public API ────────────────────────────────────────────────────────────

    def process_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        *,
        transcription: Optional[Transcription] = None,
        settings_obj: Optional[ClipSettings] = None,
        # legacy keyword args kept for backwards compat
        add_subtitles: bool = True,
        add_zoom: bool = False,
        subtitle_style: str = "modern",
    ) -> str:
        """
        Single-pass clip extraction with all enhancements chained.

        The entire pipeline runs in one FFmpeg invocation:
          fast-seek → cut → scale/pad to 9:16 → colour grade (optional)
          → speed change (optional) → subtitle burn (optional)
          + audio: loudnorm (optional) → speed (optional) → fade (optional)
        """
        if settings_obj is None:
            settings_obj = ClipSettings(
                zoom_effect=add_zoom,
                subtitle_style=subtitle_style,
            )

        duration = end_time - start_time
        stem = Path(video_path).stem
        out_name = f"{stem}_{start_time:.0f}-{end_time:.0f}_clip.mp4"
        output_path = str(self.output_dir / out_name)

        encoder = _choose_encoder(settings_obj.hardware_accel)
        res_w, res_h = _RESOLUTION_MAP.get(
            settings_obj.output_resolution, _RESOLUTION_MAP[1080]
        )

        # ── Video filter chain ────────────────────────────────────────────────
        vf_parts: List[str] = []

        # 1. Scale + pad to exact 9:16 (no black letterbox on sides from over-crop)
        vf_parts.append(
            f"scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
            f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2:black"
        )

        # 2. Speed change (video pts rescale)
        speed = settings_obj.speed
        if speed != 1.0:
            pts = round(1.0 / speed, 6)
            vf_parts.append(f"setpts={pts}*PTS")

        # 3. Colour enhancement
        if settings_obj.color_enhance:
            vf_parts.append("eq=brightness=0.03:contrast=1.1:saturation=1.2")

        # 4. Subtitle burn (inline; requires ASS file generated first)
        ass_path: Optional[str] = None
        if add_subtitles and transcription and transcription.segments:
            ass_path = output_path.replace(".mp4", ".ass")
            _generate_ass(transcription, ass_path, settings_obj.subtitle_style)
            # Escape Windows-style backslashes in the path for ffmpeg
            ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
            vf_parts.append(f"ass={ass_escaped}")

        vf = ",".join(vf_parts)

        # ── Audio filter chain ────────────────────────────────────────────────
        af_parts: List[str] = []

        # 1. Loudness normalisation (EBU R128, single-pass)
        if settings_obj.audio_normalize:
            af_parts.append("loudnorm=I=-16:TP=-1.5:LRA=11")

        # 2. Speed change for audio
        if speed != 1.0:
            # atempo range: 0.5–2.0; chain for values outside range
            tempo = speed
            atempo_filters: List[str] = []
            while tempo > 2.0:
                atempo_filters.append("atempo=2.0")
                tempo /= 2.0
            while tempo < 0.5:
                atempo_filters.append("atempo=0.5")
                tempo /= 0.5
            atempo_filters.append(f"atempo={tempo:.4f}")
            af_parts.extend(atempo_filters)

        # 3. Fade in/out
        fade = settings_obj.audio_fade_duration
        if fade > 0 and duration > fade * 2:
            out_start = max(0.0, (duration / speed) - fade)
            af_parts.append(
                f"afade=t=in:st=0:d={fade},afade=t=out:st={out_start:.3f}:d={fade}"
            )

        af = ",".join(af_parts) if af_parts else None

        # ── Build FFmpeg command ──────────────────────────────────────────────
        cmd: List[str] = [
            "ffmpeg", "-hide_banner",
            "-ss", str(start_time),      # fast seek (before -i)
            "-i", video_path,
            "-t", str(duration),
            "-vf", vf,
        ]
        if af:
            cmd += ["-af", af]

        cmd += _encoder_quality_flag(encoder, settings_obj.crf)
        cmd += [
            "-c:v", encoder,
            "-pix_fmt", "yuv420p",       # broad player compatibility
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",   # progressive web delivery
            "-y", output_path,
        ]

        try:
            logger.info(
                f"Processing clip {start_time:.1f}s–{end_time:.1f}s "
                f"(encoder={encoder}, crf={settings_obj.crf})"
            )
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise VideoProcessingError(
                    f"FFmpeg error:\n{result.stderr[-2000:]}"
                )
        except VideoProcessingError:
            raise
        except Exception as exc:
            raise VideoProcessingError(f"process_clip failed: {exc}") from exc
        finally:
            # Clean up temp ASS file
            if ass_path and Path(ass_path).exists():
                Path(ass_path).unlink(missing_ok=True)

        if not Path(output_path).exists():
            raise VideoProcessingError(f"Output clip not created: {output_path}")

        logger.info(f"Clip ready: {output_path}")
        return output_path

    def generate_thumbnail(
        self,
        video_path: str,
        timestamp: float,
        output_path: Optional[str] = None,
        width: int = 540,
    ) -> str:
        """Extract a high-quality JPEG thumbnail at the given timestamp."""
        if output_path is None:
            stem = Path(video_path).stem
            output_path = str(self.output_dir / f"{stem}_thumb_{timestamp:.0f}.jpg")

        cmd = [
            "ffmpeg", "-hide_banner",
            "-ss", str(timestamp),
            "-i", video_path,
            "-vframes", "1",
            "-vf", f"scale={width}:-2",
            "-q:v", "2",              # highest JPEG quality
            "-y", output_path,
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise VideoProcessingError(f"Thumbnail error:\n{result.stderr[-500:]}")
        except VideoProcessingError:
            raise
        except Exception as exc:
            raise VideoProcessingError(f"generate_thumbnail failed: {exc}") from exc

        logger.info(f"Thumbnail: {output_path}")
        return output_path

    def cut_clip(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None,
    ) -> str:
        """Fast stream-copy trim (no re-encode). Use for raw extraction only."""
        if output_path is None:
            stem = Path(video_path).stem
            output_path = str(
                self.output_dir / f"{stem}_{start_time:.0f}-{end_time:.0f}.mp4"
            )
        cmd = [
            "ffmpeg", "-hide_banner",
            "-ss", str(start_time),
            "-i", video_path,
            "-t", str(end_time - start_time),
            "-c", "copy",
            "-avoid_negative_ts", "1",
            "-y", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise VideoProcessingError(f"cut_clip error:\n{result.stderr[-500:]}")
        return output_path

    def convert_to_vertical(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        resolution: int = 1080,
        crf: int = 23,
    ) -> str:
        """Convert any aspect ratio to 9:16 vertical with scale+pad (no crop distortion)."""
        if output_path is None:
            stem = Path(video_path).stem
            output_path = str(self.output_dir / f"{stem}_vertical.mp4")

        res_w, res_h = _RESOLUTION_MAP.get(resolution, _RESOLUTION_MAP[1080])
        vf = (
            f"scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
            f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2:black"
        )
        cmd = [
            "ffmpeg", "-hide_banner",
            "-i", video_path,
            "-vf", vf,
            "-c:v", "libx264", "-crf", str(crf), "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-y", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise VideoProcessingError(f"convert_to_vertical error:\n{result.stderr[-500:]}")
        return output_path

    def normalize_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """Apply EBU R128 loudness normalisation (-16 LUFS target)."""
        if output_path is None:
            stem = Path(video_path).stem
            output_path = str(self.output_dir / f"{stem}_norm.mp4")
        cmd = [
            "ffmpeg", "-hide_banner",
            "-i", video_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-y", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise VideoProcessingError(f"normalize_audio error:\n{result.stderr[-500:]}")
        return output_path

    def probe(self, video_path: str) -> dict:
        """Return ffprobe JSON for the given file."""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_streams", "-show_format",
            "-of", "json", video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise VideoProcessingError(f"ffprobe failed: {result.stderr[:500]}")
        return json.loads(result.stdout)

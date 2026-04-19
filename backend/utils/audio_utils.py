"""
Audio utility functions
"""
import subprocess
import os
import numpy as np


def extract_audio(
    video_path: str,
    output_path: str,
    format: str = 'wav',
    sample_rate: int = 16000,
    channels: int = 1
) -> str:
    """
    Extract audio from video file

    Args:
        video_path: Path to video file
        output_path: Path for output audio
        format: Audio format (wav, mp3, aac)
        sample_rate: Sample rate in Hz
        channels: Number of audio channels (1 = mono, 2 = stereo)

    Returns:
        Path to extracted audio
    """
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # No video
        '-acodec', 'pcm_s16le' if format == 'wav' else 'libmp3lame',
        '-ar', str(sample_rate),
        '-ac', str(channels),
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def normalize_audio(
    audio_path: str,
    output_path: str,
    target_level: float = -16.0
) -> str:
    """
    Normalize audio to target level (LUFS)

    Args:
        audio_path: Path to source audio
        output_path: Path for output audio
        target_level: Target level in dB (default -16 LUFS)

    Returns:
        Path to normalized audio
    """
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-af', f'loudnorm=I={target_level}:TP=-1.5:LRA=11',
        '-c:a', 'pcm_s16le',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def remove_silence(
    audio_path: str,
    output_path: str,
    silence_duration: float = 0.5,
    silence_threshold: float = -50.0
) -> str:
    """
    Remove silence from audio

    Args:
        audio_path: Path to source audio
        output_path: Path for output audio
        silence_duration: Minimum silence duration to remove (seconds)
        silence_threshold: Silence threshold in dB

    Returns:
        Path to silence-removed audio
    """
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-af',
        f'silenceremove=start_periods=1:start_duration={silence_duration}:start_threshold={silence_threshold}dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration={silence_duration}:start_threshold={silence_threshold}dB:detection=peak,aformat=dblp,areverse',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def change_volume(
    audio_path: str,
    volume_change: float,
    output_path: str
) -> str:
    """
    Change audio volume

    Args:
        audio_path: Path to source audio
        volume_change: Volume multiplier (1.0 = no change, 2.0 = double, 0.5 = half)
        output_path: Path for output audio

    Returns:
        Path to volume-changed audio
    """
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-af', f'volume={volume_change}',
        '-c:a', 'pcm_s16le',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def mix_audio(
    audio_paths: list,
    output_path: str,
    weights: list = None
) -> str:
    """
    Mix multiple audio tracks

    Args:
        audio_paths: List of audio file paths
        output_path: Path for output audio
        weights: List of weights for each track (default: equal)

    Returns:
        Path to mixed audio
    """
    if weights is None:
        weights = [1.0] * len(audio_paths)

    inputs = []
    filters = []

    for i, (path, weight) in enumerate(zip(audio_paths, weights)):
        inputs.extend(['-i', path])
        filters.append(f'[{i}:0]volume={weight}[a{i}]')

    # Mix all audio
    mix_filter = f"{''.join(filters)}{''.join(f'[a{i}]' for i in range(len(audio_paths)))}amix=inputs={len(audio_paths)}:duration=first:dropout_transition=2"

    cmd = ['ffmpeg'] + inputs + ['-filter_complex', mix_filter, '-c:a', 'pcm_s16le', '-y', output_path]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def add_background_music(
    voice_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.3
) -> str:
    """
    Add background music to voice audio

    Args:
        voice_path: Path to voice audio
        music_path: Path to background music
        output_path: Path for output audio
        music_volume: Volume of background music (0.0 to 1.0)

    Returns:
        Path to mixed audio
    """
    return mix_audio([voice_path, music_path], output_path, weights=[1.0, music_volume])


def detect_silence_segments(
    audio_path: str,
    min_duration: float = 0.5,
    threshold: float = -50.0
) -> list:
    """
    Detect silence segments in audio

    Args:
        audio_path: Path to audio file
        min_duration: Minimum silence duration
        threshold: Silence threshold in dB

    Returns:
        List of (start, end) tuples
    """
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-af',
        f'silencedetect=noise={threshold}dB:d={min_duration}',
        '-f', 'null',
        '-'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    silence_segments = []
    for line in result.stderr.split('\n'):
        if 'silence_start' in line:
            start = float(line.split('silence_start:')[1].split()[0])
        elif 'silence_end' in line:
            end = float(line.split('silence_end:')[1].split()[0])
            silence_segments.append((start, end))

    return silence_segments


def get_audio_info(audio_path: str) -> dict:
    """
    Get audio file information

    Args:
        audio_path: Path to audio file

    Returns:
        Dictionary with audio metadata
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        audio_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    import json
    info = json.loads(result.stdout)

    audio_stream = None
    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'audio':
            audio_stream = stream
            break

    if not audio_stream:
        return {}

    return {
        'duration': float(info['format'].get('duration', 0)),
        'sample_rate': int(audio_stream.get('sample_rate', 0)),
        'channels': audio_stream.get('channels', 0),
        'codec': audio_stream.get('codec_name', 'unknown'),
        'bit_rate': int(audio_stream.get('bit_rate', 0))
    }


def convert_audio_format(
    audio_path: str,
    output_path: str,
    output_format: str = 'wav',
    sample_rate: int = None,
    bit_rate: str = None
) -> str:
    """
    Convert audio to different format

    Args:
        audio_path: Path to source audio
        output_path: Path for output audio
        output_format: Output format (wav, mp3, aac, etc.)
        sample_rate: Output sample rate (None = keep original)
        bit_rate: Output bit rate (e.g., '192k')

    Returns:
        Path to converted audio
    """
    cmd = ['ffmpeg', '-i', audio_path]

    if sample_rate:
        cmd.extend(['-ar', str(sample_rate)])

    if bit_rate:
        cmd.extend(['-b:a', bit_rate])

    cmd.extend(['-c:a', 'pcm_s16le' if output_format == 'wav' else 'libmp3lame', '-y', output_path])

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

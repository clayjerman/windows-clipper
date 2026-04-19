"""
Video utility functions using FFmpeg
"""
import subprocess
import os
from typing import Tuple, Optional


def get_video_info(video_path: str) -> dict:
    """
    Get video metadata using FFprobe

    Args:
        video_path: Path to video file

    Returns:
        Dictionary with video metadata
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    import json
    info = json.loads(result.stdout)

    # Extract video stream info
    video_stream = None
    audio_stream = None

    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'video' and video_stream is None:
            video_stream = stream
        elif stream.get('codec_type') == 'audio' and audio_stream is None:
            audio_stream = stream

    metadata = {
        'duration': float(info['format'].get('duration', 0)),
        'size': int(info['format'].get('size', 0)),
        'bit_rate': int(info['format'].get('bit_rate', 0)),
    }

    if video_stream:
        metadata.update({
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0)),
            'fps': eval(video_stream.get('r_frame_rate', '0/1')),
            'codec': video_stream.get('codec_name', 'unknown'),
            'pixel_format': video_stream.get('pix_fmt', 'unknown')
        })

    if audio_stream:
        metadata.update({
            'audio_codec': audio_stream.get('codec_name', 'unknown'),
            'sample_rate': int(audio_stream.get('sample_rate', 0)),
            'channels': audio_stream.get('channels', 0)
        })

    return metadata


def extract_frame(video_path: str, timestamp: float, output_path: str) -> str:
    """
    Extract a single frame from video

    Args:
        video_path: Path to video file
        timestamp: Timestamp in seconds
        output_path: Path for output image

    Returns:
        Path to extracted frame
    """
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def concat_videos(video_paths: list, output_path: str) -> str:
    """
    Concatenate multiple videos

    Args:
        video_paths: List of video file paths
        output_path: Path for output video

    Returns:
        Path to concatenated video
    """
    # Create concat list file
    list_path = output_path.replace('.mp4', '_list.txt')
    with open(list_path, 'w') as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_path,
        '-c', 'copy',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)

    # Clean up list file
    if os.path.exists(list_path):
        os.remove(list_path)

    return output_path


def resize_video(
    video_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> str:
    """
    Resize video to specific dimensions

    Args:
        video_path: Path to source video
        output_path: Path for output video
        width: Target width (None = keep aspect ratio)
        height: Target height (None = keep aspect ratio)

    Returns:
        Path to resized video
    """
    scale_filter = ''
    if width and height:
        scale_filter = f'scale={width}:{height}'
    elif width:
        scale_filter = f'scale={width}:-1'
    elif height:
        scale_filter = f'scale=-1:{height}'

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', scale_filter,
        '-c:a', 'copy',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def add_watermark(
    video_path: str,
    watermark_path: str,
    output_path: str,
    position: str = 'bottom_right'
) -> str:
    """
    Add watermark to video

    Args:
        video_path: Path to source video
        watermark_path: Path to watermark image
        output_path: Path for output video
        position: Watermark position (top_left, top_right, bottom_left, bottom_right)

    Returns:
        Path to watermarked video
    """
    position_map = {
        'top_left': '10:10',
        'top_right': 'W-w-10:10',
        'bottom_left': '10:H-h-10',
        'bottom_right': 'W-w-10:H-h-10'
    }

    overlay_pos = position_map.get(position, position_map['bottom_right'])

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-i', watermark_path,
        '-filter_complex',
        f'[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay={overlay_pos}',
        '-c:a', 'copy',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def trim_video(
    video_path: str,
    start_time: float,
    duration: float,
    output_path: str
) -> str:
    """
    Trim video to specific duration

    Args:
        video_path: Path to source video
        start_time: Start time in seconds
        duration: Duration in seconds
        output_path: Path for output video

    Returns:
        Path to trimmed video
    """
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-t', str(duration),
        '-i', video_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-crf', '23',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def change_speed(video_path: str, speed_factor: float, output_path: str) -> str:
    """
    Change video playback speed

    Args:
        video_path: Path to source video
        speed_factor: Speed multiplier (0.5 = half speed, 2.0 = double speed)
        output_path: Path for output video

    Returns:
        Path to speed-changed video
    """
    if speed_factor == 1.0:
        return video_path

    # Setpts filter for video, atempo filter for audio
    video_filter = f'setpts={1.0/speed_factor}*PTS'
    audio_filter = f'atempo={speed_factor}'

    # Need to chain atempo for extreme values (atempo only supports 0.5 to 2.0)
    if speed_factor < 0.5:
        audio_filter = f'atempo=0.5,atempo={speed_factor/0.5}'
    elif speed_factor > 2.0:
        audio_filter = f'atempo=2.0,atempo={speed_factor/2.0}'

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-filter_complex',
        f'[0:v]{video_filter}[v];[0:a]{audio_filter}[a]',
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-crf', '23',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def add_fade(
    video_path: str,
    fade_in_duration: float = 0,
    fade_out_duration: float = 0,
    output_path: str
) -> str:
    """
    Add fade in/out to video

    Args:
        video_path: Path to source video
        fade_in_duration: Fade in duration in seconds
        fade_out_duration: Fade out duration in seconds
        output_path: Path for output video

    Returns:
        Path to faded video
    """
    filters = []

    if fade_in_duration > 0:
        filters.append(f'fade=t=in:st=0:d={fade_in_duration}')

    if fade_out_duration > 0:
        filters.append(f'fade=t=out:st={get_video_duration(video_path) - fade_out_duration}:d={fade_out_duration}')

    if not filters:
        return video_path

    video_filter = ','.join(filters)

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', video_filter,
        '-c:a', 'copy',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def get_video_duration(video_path: str) -> float:
    """
    Get video duration in seconds

    Args:
        video_path: Path to video file

    Returns:
        Duration in seconds
    """
    info = get_video_info(video_path)
    return info['duration']


def create_video_from_images(
    image_paths: list,
    output_path: str,
    duration_per_image: float = 2.0,
    fps: int = 30
) -> str:
    """
    Create video from sequence of images

    Args:
        image_paths: List of image file paths
        output_path: Path for output video
        duration_per_image: Duration each image is shown
        fps: Frames per second

    Returns:
        Path to created video
    """
    # Create concat file with duration
    list_path = output_path.replace('.mp4', '_list.txt')
    with open(list_path, 'w') as f:
        for path in image_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
            f.write(f"duration {duration_per_image}\n")

    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_path,
        '-vf', 'fps=30',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-y', output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)

    if os.path.exists(list_path):
        os.remove(list_path)

    return output_path

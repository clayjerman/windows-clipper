"""
File utility functions
"""
import os
import shutil
import hashlib
from typing import List, Optional
from pathlib import Path


def ensure_directory(directory: str) -> str:
    """
    Ensure directory exists, create if not

    Args:
        directory: Directory path

    Returns:
        Directory path
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


def get_file_hash(file_path: str, algorithm: str = 'md5') -> str:
    """
    Calculate file hash

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha256, etc.)

    Returns:
        Hash string
    """
    hash_func = hashlib.new(algorithm)

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def get_file_size(file_path: str, unit: str = 'bytes') -> float:
    """
    Get file size in specified unit

    Args:
        file_path: Path to file
        unit: Size unit (bytes, kb, mb, gb)

    Returns:
        File size
    """
    if not os.path.exists(file_path):
        return 0.0

    size_bytes = os.path.getsize(file_path)

    units = {
        'bytes': 1,
        'kb': 1024,
        'mb': 1024 ** 2,
        'gb': 1024 ** 3
    }

    return size_bytes / units.get(unit.lower(), 1)


def clean_directory(
    directory: str,
    pattern: str = '*',
    max_age_days: Optional[int] = None
) -> int:
    """
    Clean directory by removing files matching pattern

    Args:
        directory: Directory path
        pattern: File pattern (glob)
        max_age_days: Maximum file age in days (None = no age limit)

    Returns:
        Number of files deleted
    """
    import time
    import glob

    deleted = 0
    cutoff_time = None

    if max_age_days:
        cutoff_time = time.time() - (max_age_days * 86400)

    for file_path in glob.glob(os.path.join(directory, pattern)):
        try:
            if max_age_days and cutoff_time:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime > cutoff_time:
                    continue

            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted += 1
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                deleted += 1

        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

    return deleted


def get_directory_size(directory: str) -> dict:
    """
    Get directory size statistics

    Args:
        directory: Directory path

    Returns:
        Dictionary with size statistics
    """
    total_size = 0
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(directory):
        dir_count += len(dirs)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
                file_count += 1
            except OSError:
                pass

    return {
        'total_bytes': total_size,
        'total_mb': round(total_size / (1024 ** 2), 2),
        'file_count': file_count,
        'directory_count': dir_count
    }


def copy_file(
    source: str,
    destination: str,
    overwrite: bool = False
) -> str:
    """
    Copy file from source to destination

    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Overwrite if exists

    Returns:
        Destination file path
    """
    if not overwrite and os.path.exists(destination):
        raise FileExistsError(f"File already exists: {destination}")

    ensure_directory(os.path.dirname(destination))
    shutil.copy2(source, destination)

    return destination


def move_file(
    source: str,
    destination: str,
    overwrite: bool = False
) -> str:
    """
    Move file from source to destination

    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Overwrite if exists

    Returns:
        Destination file path
    """
    if not overwrite and os.path.exists(destination):
        raise FileExistsError(f"File already exists: {destination}")

    ensure_directory(os.path.dirname(destination))
    shutil.move(source, destination)

    return destination


def find_files_by_extension(
    directory: str,
    extensions: List[str],
    recursive: bool = True
) -> List[str]:
    """
    Find files by extension in directory

    Args:
        directory: Directory to search
        extensions: List of file extensions (with dots, e.g., ['.mp4', '.avi'])
        recursive: Search recursively

    Returns:
        List of file paths
    """
    found = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in [ext.lower() for ext in extensions]:
                found.append(os.path.join(root, file))

        if not recursive:
            break

    return found


def get_unique_filename(directory: str, filename: str) -> str:
    """
    Get unique filename in directory (adds counter if exists)

    Args:
        directory: Directory path
        filename: Original filename

    Returns:
        Unique filename
    """
    name, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{name}_{counter}{ext}"
        counter += 1

    return filename


def read_file_as_base64(file_path: str) -> str:
    """
    Read file as base64 encoded string

    Args:
        file_path: Path to file

    Returns:
        Base64 encoded string
    """
    import base64

    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def write_base64_to_file(content: str, file_path: str) -> str:
    """
    Write base64 encoded content to file

    Args:
        content: Base64 encoded string
        file_path: Path to output file

    Returns:
        File path
    """
    import base64

    ensure_directory(os.path.dirname(file_path))

    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(content))

    return file_path


def compress_directory(
    directory: str,
    output_path: str
) -> str:
    """
    Compress directory to ZIP file

    Args:
        directory: Directory to compress
        output_path: Path for ZIP file

    Returns:
        ZIP file path
    """
    import zipfile

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)

    return output_path


def extract_archive(
    archive_path: str,
    output_directory: str
) -> str:
    """
    Extract archive to directory

    Args:
        archive_path: Path to archive (ZIP)
        output_directory: Output directory

    Returns:
        Output directory path
    """
    import zipfile

    ensure_directory(output_directory)

    with zipfile.ZipFile(archive_path, 'r') as zipf:
        zipf.extractall(output_directory)

    return output_directory


def get_video_files(directory: str) -> List[str]:
    """
    Get all video files in directory

    Args:
        directory: Directory path

    Returns:
        List of video file paths
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.wmv']
    return find_files_by_extension(directory, video_extensions)


def get_audio_files(directory: str) -> List[str]:
    """
    Get all audio files in directory

    Args:
        directory: Directory path

    Returns:
        List of audio file paths
    """
    audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma']
    return find_files_by_extension(directory, audio_extensions)


def get_image_files(directory: str) -> List[str]:
    """
    Get all image files in directory

    Args:
        directory: Directory path

    Returns:
        List of image file paths
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    return find_files_by_extension(directory, image_extensions)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing/replacing invalid characters

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Replace invalid characters with underscore
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # If empty, use default
    if not filename:
        filename = 'unnamed'

    return filename

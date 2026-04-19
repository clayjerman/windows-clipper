"""
Face and mouth detection using MediaPipe
"""
import os
import logging
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from ..core.config import settings
from ..models.clip import SpeakerInfo

logger = logging.getLogger(__name__)


@dataclass
class FaceDetection:
    """Face detection result"""
    face_id: int
    bounding_box: Tuple[int, int, int, int]  # x, y, width, height
    confidence: float
    landmarks: np.ndarray  # 468 face mesh landmarks
    mouth_open: float  # 0-1, how open the mouth is


@dataclass
class SpeakerTracking:
    """Speaker tracking over time"""
    face_id: int
    speaking_probability: float  # 0-1
    mouth_movement_intensity: float  # 0-1
    is_speaking: bool


class FaceDetector:
    """Detect faces using MediaPipe Face Detection"""

    def __init__(self):
        """Initialize MediaPipe Face Detection"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize detectors
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        logger.info("Face detector initialized")

    def detect_faces(self, frame: np.ndarray) -> List[FaceDetection]:
        """
        Detect faces in a frame

        Args:
            frame: Video frame (BGR format)

        Returns:
            List of FaceDetection objects
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = self.face_detection.process(rgb_frame)

        detections = []

        if results.detections:
            for idx, detection in enumerate(results.detections):
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape

                x = int(bbox.xcenter * w - bbox.width * w / 2)
                y = int(bbox.ycenter * h - bbox.height * h / 2)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                # Get face mesh landmarks for mouth detection
                mesh_results = self.face_mesh.process(rgb_frame)

                landmarks = None
                mouth_open = 0.0

                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        landmarks = np.array([[lm.x, lm.y] for lm in face_landmarks.landmark])
                        mouth_open = self._calculate_mouth_openness(landmarks)
                        break  # Just take first face mesh

                detections.append(FaceDetection(
                    face_id=idx,
                    bounding_box=(x, y, width, height),
                    confidence=detection.score[0],
                    landmarks=landmarks,
                    mouth_open=mouth_open
                ))

        return detections

    def _calculate_mouth_openness(self, landmarks: np.ndarray) -> float:
        """
        Calculate how open the mouth is using face mesh landmarks

        Args:
            landmarks: 468 face mesh landmarks

        Returns:
            Mouth openness (0-1)
        """
        if landmarks is None or len(landmarks) < 468:
            return 0.0

        # Key mouth landmarks (upper and lower lip)
        upper_lip = landmarks[13]  # Upper lip
        lower_lip = landmarks[14]  # Lower lip

        # Calculate distance
        distance = np.linalg.norm(upper_lip - lower_lip)

        # Normalize (typical range is 0.01 to 0.1)
        openness = np.clip(distance * 15, 0.0, 1.0)

        return openness


class MouthTracker:
    """Track mouth movement to detect speaking"""

    def __init__(self):
        """Initialize mouth tracker"""
        self.face_detector = FaceDetector()
        self.mouth_history: Dict[int, List[float]] = {}  # Track mouth openness over time
        self.window_size = 10  # Frames to analyze

    def process_frame(self, frame: np.ndarray, frame_idx: int) -> List[SpeakerTracking]:
        """
        Process a single frame and detect speakers

        Args:
            frame: Video frame (BGR format)
            frame_idx: Frame index for tracking

        Returns:
            List of SpeakerTracking objects
        """
        # Detect faces
        faces = self.face_detector.detect_faces(frame)

        tracking = []

        for face in faces:
            # Update mouth history
            if face.face_id not in self.mouth_history:
                self.mouth_history[face.face_id] = []

            self.mouth_history[face.face_id].append(face.mouth_open)

            # Keep only recent frames
            if len(self.mouth_history[face.face_id]) > self.window_size:
                self.mouth_history[face.face_id].pop(0)

            # Calculate speaking probability
            speaking_prob = self._calculate_speaking_probability(face.face_id)

            # Determine if speaking
            is_speaking = speaking_prob > 0.3

            # Calculate movement intensity
            movement_intensity = self._calculate_movement_intensity(face.face_id)

            tracking.append(SpeakerTracking(
                face_id=face.face_id,
                speaking_probability=speaking_prob,
                mouth_movement_intensity=movement_intensity,
                is_speaking=is_speaking
            ))

        return tracking

    def _calculate_speaking_probability(self, face_id: int) -> float:
        """Calculate probability that face is speaking"""
        if face_id not in self.mouth_history:
            return 0.0

        history = self.mouth_history[face_id]

        if len(history) < 5:
            return 0.0

        # Calculate variance in mouth openness (speaking = more variation)
        variance = np.var(history)

        # Normalize to probability
        probability = np.clip(variance * 50, 0.0, 1.0)

        return probability

    def _calculate_movement_intensity(self, face_id: int) -> float:
        """Calculate mouth movement intensity"""
        if face_id not in self.mouth_history:
            return 0.0

        history = self.mouth_history[face_id]

        if len(history) < 2:
            return 0.0

        # Calculate total movement
        total_movement = sum(abs(history[i] - history[i-1]) for i in range(1, len(history)))

        # Normalize
        intensity = np.clip(total_movement * 2, 0.0, 1.0)

        return intensity

    def get_active_speaker(self, frame: np.ndarray, frame_idx: int) -> Optional[SpeakerInfo]:
        """
        Get the active speaker in a frame

        Args:
            frame: Video frame (BGR format)
            frame_idx: Frame index

        Returns:
            SpeakerInfo of the active speaker, or None
        """
        tracking_results = self.process_frame(frame, frame_idx)

        if not tracking_results:
            return None

        # Find face with highest speaking probability
        active = max(tracking_results, key=lambda t: t.speaking_probability)

        # Get face detection
        faces = self.face_detector.detect_faces(frame)
        active_face = next((f for f in faces if f.face_id == active.face_id), None)

        if not active_face:
            return None

        return SpeakerInfo(
            face_id=active.face_id,
            confidence=active_face.confidence,
            bounding_box=list(active_face.bounding_box),
            mouth_active=active.is_speaking,
            speaking_probability=active.speaking_probability
        )

    def track_video(self, video_path: str, sample_rate: int = 5) -> List[Tuple[int, SpeakerInfo]]:
        """
        Track speakers throughout a video

        Args:
            video_path: Path to video file
            sample_rate: Sample every N frames (for performance)

        Returns:
            List of (frame_idx, SpeakerInfo) tuples
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return []

        tracking_data = []
        frame_count = 0

        logger.info(f"Tracking speakers in: {video_path}")

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                # Sample frames
                if frame_count % sample_rate == 0:
                    speaker_info = self.get_active_speaker(frame, frame_count)

                    if speaker_info:
                        tracking_data.append((frame_count, speaker_info))

                frame_count += 1

                if frame_count % 100 == 0:
                    logger.info(f"Processed {frame_count} frames...")

        finally:
            cap.release()

        logger.info(f"Speaker tracking complete: {len(tracking_data)} frames with speakers")
        return tracking_data

    def generate_crop_coordinates(
        self,
        frame_shape: Tuple[int, int, int],
        speaker_info: SpeakerInfo,
        target_aspect: str = "9:16"
    ) -> Tuple[int, int, int, int]:
        """
        Generate crop coordinates to focus on active speaker

        Args:
            frame_shape: (height, width, channels) of frame
            speaker_info: Speaker detection info
            target_aspect: Target aspect ratio (e.g., "9:16")

        Returns:
            (x, y, width, height) crop coordinates
        """
        h, w, _ = frame_shape

        # Parse aspect ratio
        if ":" in target_aspect:
            ar_w, ar_h = map(int, target_aspect.split(":"))
        else:
            ar_w, ar_h = 9, 16

        # Get speaker bounding box
        bbox = speaker_info.bounding_box
        speaker_x, speaker_y, speaker_w, speaker_h = bbox

        # Calculate crop size
        if ar_h > ar_w:  # Portrait orientation
            crop_width = min(w, int(h * ar_w / ar_h))
            crop_height = h
        else:  # Landscape orientation
            crop_width = w
            crop_height = min(h, int(w * ar_h / ar_w))

        # Center crop on speaker
        center_x = speaker_x + speaker_w // 2
        x = max(0, min(center_x - crop_width // 2, w - crop_width))
        y = 0

        return (x, y, crop_width, crop_height)

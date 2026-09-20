"""Application configuration for HandFace Follow RPS."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Runtime settings kept in one place for easy tuning."""

    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720
    mirror_frame: bool = True

    max_num_hands: int = 2
    hand_detection_confidence: float = 0.65
    hand_tracking_confidence: float = 0.60
    face_detection_confidence: float = 0.60

    # Finger and gesture thresholds. Values use MediaPipe normalized coordinates.
    extended_finger_angle_degrees: float = 155.0
    min_finger_distance_gain: float = 1.05
    wave_history_seconds: float = 1.6
    wave_min_samples: int = 8
    wave_min_x_span: float = 0.10
    wave_min_direction_changes: int = 2
    wave_motion_epsilon: float = 0.015

    fps_smoothing: float = 0.90


WINDOW_NAME = "HandFace Follow RPS"

COLOR_FACE = (80, 220, 255)
COLOR_HAND = (90, 255, 120)
COLOR_TEXT = (245, 245, 245)
COLOR_ACCENT = (60, 140, 255)
COLOR_WARNING = (40, 80, 255)

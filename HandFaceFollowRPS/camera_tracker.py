"""Camera IO plus MediaPipe face and hand tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import mediapipe as mp

from config import (
    AppConfig,
    COLOR_ACCENT,
    COLOR_FACE,
    COLOR_HAND,
    COLOR_TEXT,
    COLOR_WARNING,
)


@dataclass
class HandObservation:
    """One detected hand and its metadata."""

    landmarks: object
    handedness_label: str
    handedness_score: float


@dataclass
class TrackingResult:
    """Vision results for a single frame."""

    face_detection: Optional[object]
    hands: List[HandObservation]


class CameraStream:
    """Small wrapper around OpenCV webcam capture."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.capture: Optional[cv2.VideoCapture] = None

    def open(self) -> None:
        self.capture = cv2.VideoCapture(self.config.camera_index)
        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open webcam index {self.config.camera_index}. "
                "Check camera permissions or change AppConfig.camera_index."
            )

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.frame_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)

    def read(self) -> Tuple[bool, Optional[object]]:
        if self.capture is None:
            return False, None

        ok, frame = self.capture.read()
        if not ok or frame is None:
            return False, None

        if self.config.mirror_frame:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None


class PersonTracker:
    """Tracks the primary visible face and visible hands in each frame."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.max_num_hands,
            model_complexity=1,
            min_detection_confidence=config.hand_detection_confidence,
            min_tracking_confidence=config.hand_tracking_confidence,
        )
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=config.face_detection_confidence,
        )

    def process(self, frame_bgr: object) -> TrackingResult:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False

        face_results = self.face_detection.process(frame_rgb)
        hand_results = self.hands.process(frame_rgb)

        hands: List[HandObservation] = []
        if hand_results.multi_hand_landmarks:
            for index, landmarks in enumerate(hand_results.multi_hand_landmarks):
                label = f"Hand {index + 1}"
                score = 0.0
                if hand_results.multi_handedness and index < len(hand_results.multi_handedness):
                    handedness = hand_results.multi_handedness[index].classification[0]
                    label = handedness.label
                    score = handedness.score
                hands.append(HandObservation(landmarks, label, score))

        face_detection = None
        if face_results.detections:
            face_detection = max(
                face_results.detections,
                key=lambda detection: detection.score[0] if detection.score else 0.0,
            )

        return TrackingResult(face_detection=face_detection, hands=hands)

    def close(self) -> None:
        self.hands.close()
        self.face_detection.close()


def draw_tracking_overlay(
    frame_bgr: object,
    tracker: PersonTracker,
    result: TrackingResult,
    gesture_labels: List[str],
    fps: float,
) -> object:
    """Draw face box, hand landmarks, status text, and current gesture labels."""

    height, width = frame_bgr.shape[:2]

    if result.face_detection is not None:
        _draw_face_detection(frame_bgr, result.face_detection, width, height)

    for hand in result.hands:
        tracker.mp_drawing.draw_landmarks(
            frame_bgr,
            hand.landmarks,
            tracker.mp_hands.HAND_CONNECTIONS,
            tracker.mp_styles.get_default_hand_landmarks_style(),
            tracker.mp_styles.get_default_hand_connections_style(),
        )

    if result.hands:
        status = f"Tracking: face {'yes' if result.face_detection else 'no'} | hands {len(result.hands)}"
    else:
        status = f"Tracking: face {'yes' if result.face_detection else 'no'} | hands 0"

    gesture_text = "Gesture: " + (", ".join(gesture_labels) if gesture_labels else "None")
    _draw_label(frame_bgr, status, (18, 34), COLOR_ACCENT)
    _draw_label(frame_bgr, gesture_text, (18, 74), COLOR_HAND if gesture_labels else COLOR_WARNING)
    _draw_label(frame_bgr, f"FPS: {fps:0.1f}", (18, 114), COLOR_TEXT)
    _draw_label(frame_bgr, "Press Q or Esc to quit", (18, height - 22), COLOR_TEXT)

    return frame_bgr


def _draw_face_detection(frame_bgr: object, detection: object, width: int, height: int) -> None:
    bbox = detection.location_data.relative_bounding_box
    x = max(0, int(bbox.xmin * width))
    y = max(0, int(bbox.ymin * height))
    w = min(width - x, int(bbox.width * width))
    h = min(height - y, int(bbox.height * height))
    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), COLOR_FACE, 2)
    cv2.putText(
        frame_bgr,
        "Face",
        (x, max(24, y - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        COLOR_FACE,
        2,
        cv2.LINE_AA,
    )

    for keypoint in detection.location_data.relative_keypoints:
        px = int(keypoint.x * width)
        py = int(keypoint.y * height)
        cv2.circle(frame_bgr, (px, py), 3, COLOR_FACE, -1)


def _draw_label(frame_bgr: object, text: str, origin: Tuple[int, int], color: Tuple[int, int, int]) -> None:
    x, y = origin
    cv2.putText(
        frame_bgr,
        text,
        (x + 1, y + 1),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        3,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame_bgr,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
        cv2.LINE_AA,
    )

"""Rule-based hand gesture recognition for Rock, Paper, Scissors, and Hi."""

from __future__ import annotations

import math
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple

from config import AppConfig


WRIST = 0
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_MCP = 5
INDEX_PIP = 6
INDEX_TIP = 8
MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_TIP = 12
RING_MCP = 13
RING_PIP = 14
RING_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_TIP = 20


@dataclass(frozen=True)
class GestureResult:
    """Gesture output for one hand."""

    gesture: str
    fingers: Dict[str, bool]
    hand_center: Tuple[float, float]


class GestureRecognizer:
    """Classifies static finger poses and detects waving over time."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.wave_history: Dict[str, Deque[Tuple[float, float]]] = defaultdict(deque)

    def classify(self, hand_id: str, landmarks: object) -> GestureResult:
        points = [(point.x, point.y, point.z) for point in landmarks.landmark]
        fingers = self._extended_fingers(points)
        center = self._hand_center(points)

        gesture = self._static_gesture(fingers)
        if gesture == "Paper" and self._is_waving(hand_id, center[0], time.monotonic()):
            gesture = "Hi"

        return GestureResult(gesture=gesture, fingers=fingers, hand_center=center)

    def _extended_fingers(self, points: List[Tuple[float, float, float]]) -> Dict[str, bool]:
        return {
            "thumb": self._thumb_is_extended(points),
            "index": self._finger_is_extended(points, INDEX_MCP, INDEX_PIP, INDEX_TIP),
            "middle": self._finger_is_extended(points, MIDDLE_MCP, MIDDLE_PIP, MIDDLE_TIP),
            "ring": self._finger_is_extended(points, RING_MCP, RING_PIP, RING_TIP),
            "pinky": self._finger_is_extended(points, PINKY_MCP, PINKY_PIP, PINKY_TIP),
        }

    def _finger_is_extended(
        self,
        points: List[Tuple[float, float, float]],
        mcp_index: int,
        pip_index: int,
        tip_index: int,
    ) -> bool:
        # A finger is extended when it is mostly straight and the tip is farther
        # from the wrist than the middle joint. This is more rotation-tolerant
        # than checking only y-position.
        angle = _angle_degrees(points[mcp_index], points[pip_index], points[tip_index])
        tip_distance = _distance_2d(points[WRIST], points[tip_index])
        pip_distance = _distance_2d(points[WRIST], points[pip_index])
        return (
            angle >= self.config.extended_finger_angle_degrees
            and tip_distance >= pip_distance * self.config.min_finger_distance_gain
        )

    def _thumb_is_extended(self, points: List[Tuple[float, float, float]]) -> bool:
        # Thumb direction varies the most by hand rotation, so use straightness
        # plus distance from the wrist instead of a left/right x-coordinate rule.
        angle = _angle_degrees(points[THUMB_MCP], points[THUMB_IP], points[THUMB_TIP])
        tip_distance = _distance_2d(points[WRIST], points[THUMB_TIP])
        ip_distance = _distance_2d(points[WRIST], points[THUMB_IP])
        return (
            angle >= self.config.extended_finger_angle_degrees - 8.0
            and tip_distance >= ip_distance * 1.03
        )

    @staticmethod
    def _hand_center(points: List[Tuple[float, float, float]]) -> Tuple[float, float]:
        palm_indices = [WRIST, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]
        x = sum(points[index][0] for index in palm_indices) / len(palm_indices)
        y = sum(points[index][1] for index in palm_indices) / len(palm_indices)
        return x, y

    @staticmethod
    def _static_gesture(fingers: Dict[str, bool]) -> str:
        extended_count = sum(1 for is_extended in fingers.values() if is_extended)

        if extended_count == 5:
            return "Paper"

        if extended_count == 0:
            return "Rock"

        if (
            fingers["index"]
            and fingers["middle"]
            and not fingers["ring"]
            and not fingers["pinky"]
            and extended_count <= 3
        ):
            return "Scissors"

        return "Unknown"

    def _is_waving(self, hand_id: str, center_x: float, now: float) -> bool:
        history = self.wave_history[hand_id]
        history.append((now, center_x))

        while history and now - history[0][0] > self.config.wave_history_seconds:
            history.popleft()

        if len(history) < self.config.wave_min_samples:
            return False

        x_values = [x for _, x in history]
        x_span = max(x_values) - min(x_values)
        if x_span < self.config.wave_min_x_span:
            return False

        directions: List[int] = []
        previous_x = x_values[0]
        for x in x_values[1:]:
            delta = x - previous_x
            previous_x = x
            if abs(delta) < self.config.wave_motion_epsilon:
                continue
            directions.append(1 if delta > 0 else -1)

        changes = 0
        previous_direction = None
        for direction in directions:
            if previous_direction is not None and direction != previous_direction:
                changes += 1
            previous_direction = direction

        return changes >= self.config.wave_min_direction_changes


def _distance_2d(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _angle_degrees(
    a: Tuple[float, float, float],
    b: Tuple[float, float, float],
    c: Tuple[float, float, float],
) -> float:
    """Return angle ABC in degrees."""

    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.hypot(*ba)
    mag_bc = math.hypot(*bc)
    if mag_ba == 0.0 or mag_bc == 0.0:
        return 0.0
    cosine = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    return math.degrees(math.acos(cosine))

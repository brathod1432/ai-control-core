"""Main entry point for HandFace Follow RPS."""

from __future__ import annotations

import sys
import time

try:
    import cv2

    from camera_tracker import CameraStream, PersonTracker, draw_tracking_overlay
    from config import AppConfig, WINDOW_NAME
    from gesture_recognition import GestureRecognizer
except ImportError as exc:
    print("Missing dependency:", exc)
    print("Install dependencies with: python -m pip install -r requirements.txt")
    sys.exit(1)


def run() -> int:
    config = AppConfig()
    camera = CameraStream(config)
    tracker = None

    try:
        camera.open()
        tracker = PersonTracker(config)
        recognizer = GestureRecognizer(config)

        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

        fps = 0.0
        previous_time = time.perf_counter()

        while True:
            ok, frame = camera.read()
            if not ok or frame is None:
                print("Camera frame could not be read. Exiting.")
                return 2

            result = tracker.process(frame)
            gesture_labels = []
            for index, hand in enumerate(result.hands):
                hand_id = f"{hand.handedness_label}-{index}"
                gesture = recognizer.classify(hand_id, hand.landmarks)
                if gesture.gesture != "Unknown":
                    gesture_labels.append(f"{hand.handedness_label}: {gesture.gesture}")

            now = time.perf_counter()
            instant_fps = 1.0 / max(now - previous_time, 1e-6)
            previous_time = now
            fps = instant_fps if fps == 0.0 else (
                config.fps_smoothing * fps + (1.0 - config.fps_smoothing) * instant_fps
            )

            draw_tracking_overlay(frame, tracker, result, gesture_labels, fps)
            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q"), ord("Q")):
                return 0

    except RuntimeError as exc:
        print(exc)
        return 1
    finally:
        camera.release()
        if tracker is not None:
            tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    raise SystemExit(run())

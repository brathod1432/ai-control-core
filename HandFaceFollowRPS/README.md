# HandFace Follow RPS

HandFace Follow RPS is a local Python webcam app that tracks the primary visible face and one or two visible hands, then labels simple real-time gestures:

- Open hand with five extended fingers: `Paper`
- Closed fist: `Rock`
- Index and middle fingers raised: `Scissors`
- Open hand moving side to side over several frames: `Hi`

The app uses OpenCV for webcam capture and drawing, MediaPipe for face and hand detection/tracking, and a small rule-based gesture recognizer for readable, tunable logic.

## Project Structure

```text
HandFaceFollowRPS/
├── main.py
├── camera_tracker.py
├── gesture_recognition.py
├── config.py
├── requirements.txt
└── README.md
```

## Setup

Use Python 3.10 or newer. A virtual environment is recommended.

```powershell
cd C:\Users\kbrat\PycharmProjects\ai-control-core\HandFaceFollowRPS
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

The webcam starts automatically. Stand in front of the camera and show one hand clearly. Press `Q` or `Esc` to exit.

## Gesture Logic

The recognizer first determines whether each finger is extended. For the four long fingers, it checks that the finger is mostly straight and that the fingertip is farther from the wrist than the middle joint. The thumb uses a similar straightness and distance check because its direction changes more with hand rotation.

Static gesture rules:

- `Paper`: all five fingers are extended.
- `Rock`: no fingers are extended.
- `Scissors`: index and middle are extended while ring and pinky are folded.

Wave detection is temporal. When the static pose is `Paper`, the app stores recent hand-center x positions and labels `Hi` only when there is enough side-to-side travel and at least two direction changes inside the rolling time window.

## Troubleshooting

- If the webcam cannot open, check camera permissions or change `camera_index` in `config.py`.
- If imports fail, run `python -m pip install -r requirements.txt`.
- If gestures feel too strict or loose, tune thresholds in `config.py`.

## Possible Improvements

- Add gesture smoothing with majority voting over the last few labels.
- Add explicit primary-person selection when multiple people are visible.
- Add per-hand calibration for different camera angles.
- Add a small GUI panel for threshold tuning.
- Add tests around synthetic landmark patterns for gesture classification.

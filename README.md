# TheftAlert

# Real-time motion and theft detection system using OpenCV and video analysis.

# Demo Motion Detection System

![Demo GIF](output_demo.gif)

## Overview

Demo Motion Detection System is a **real-time motion detection application** built using Python and OpenCV. It supports webcam and video file input, detects moving objects, and visualizes them with bounding boxes.

## Features

- Real-time motion detection
- Bounding box for moving objects
- Adjustable minimum area threshold
- Timestamp and status overlay
- Easy to use with webcam or video files

## Installation

```bash
git clone https://github.com/yourusername/DemoMotionDetection.git
cd DemoMotionDetection
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install opencv-python imutils
```

## Usage

Run on live webcam feed:

```bash
python demo.py
```

Run on a video file:

```bash
python demo.py --video path/to/video.mp4 --min-area 400
```

Optional argument:

- `--min-area` : minimum contour area to detect (default 500)

## How it Works

1. Capture frame from webcam or video.
2. Resize, convert to grayscale, and blur.
3. Compute absolute difference with first frame.
4. Apply threshold and dilation.
5. Find contours and draw bounding boxes for significant motion.
6. Overlay room status and timestamp.

## Notes

- Press `q` to quit.
- Adjust `--min-area` for sensitivity.

## License

MIT License

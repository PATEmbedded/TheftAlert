# TheftAlert: Real-time motion detection for security monitoring
# Requirements: pip install opencv-python imutils

import argparse
import datetime
import time

import cv2
import imutils
from imutils.video import VideoStream

# ------------------------------
# Argument Parsing
# ------------------------------
ap = argparse.ArgumentParser(description="TheftAlert: Real-time motion detection")
ap.add_argument("-v", "--video", help="Path to the input video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="Minimum area size for motion detection")
args = vars(ap.parse_args())

# ------------------------------
# Initialize Video Stream
# ------------------------------
if args.get("video") is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["video"])

# ------------------------------
# Initialize first frame
# ------------------------------
first_frame = None

# ------------------------------
# Main loop
# ------------------------------
while True:
    # Grab current frame
    frame = vs.read()
    frame = frame if args.get("video") is None else frame[1]
    text = "Unoccupied"

    # End of video
    if frame is None:
        break

    # Resize, convert to grayscale, blur
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize first frame
    if first_frame is None:
        first_frame = gray
        continue

    # Compute difference between first frame and current frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Check contours for motion
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    # Draw status and timestamp
    cv2.putText(frame, f"Room Status: {text}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # Display frames
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frame_delta)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# ------------------------------
# Cleanup
# ------------------------------
vs.stop() if args.get("video") is None else vs.release()
cv2.destroyAllWindows()

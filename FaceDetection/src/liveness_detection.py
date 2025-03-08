import os
import math
import cvzone
import cv2
import numpy as np
import mediapipe as mp
from ultralytics import YOLO

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load the model once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/n_version3_25best.pt")
model = YOLO(MODEL_PATH)
classNames = ["fake", "real"]

confidence=0.8
# Motion detection variables
prev_frame = None
motion_threshold = 1500


def detect_motion(frame):
    """Detects motion by comparing the current frame with the previous frame."""
    global prev_frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # No motion detected in the first frame
    if prev_frame is None:
        prev_frame = gray
        return False  

    # Compute the absolute difference between the current frame and previous frame
    frame_diff = cv2.absdiff(prev_frame, gray)
    prev_frame = gray

    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    motion_score = np.sum(thresh)

    motion_detected = motion_score > motion_threshold

    return motion_detected

def identify_real_or_fake(frame):
    motion_detected = detect_motion(frame)
    results = model(frame, stream=True, verbose=False)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            
            if conf > confidence:
                identification = classNames[cls]
                if identification == 'real':
                    if not motion_detected:
                        identification = 'fake'

                color = (0, 255, 0) if identification == 'real' else (0, 0, 255)
                cvzone.cornerRect(frame, (x1, y1, w, h), colorC=color, colorR=color)
                cvzone.putTextRect(frame, f'{identification.upper()} {int(conf*100)}%',
                                   (max(0, x1), max(35, y1)), scale=2, thickness=4, colorR=color,
                                   colorB=color)
                return identification  # Return "real" or "fake"
    
    return None  # Return None if no valid prediction is made
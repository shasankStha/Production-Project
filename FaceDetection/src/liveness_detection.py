import os
import math
import cvzone
import cv2
import numpy as np
import mediapipe as mp
from ultralytics import YOLO
import time

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
prev_landmarks = None
motion_threshold = 3.0  # Threshold for face motion (sum of distances)
motion_score_history = []  # Stores motion scores for a rolling average
motion_window = 10  # Number of frames to average motion
motion_detected_flag = False


def detect_motion(frame):
    """Detects motion by comparing the current frame with the previous frame."""
    global prev_landmarks, motion_score_history, motion_detected_flag

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if not results.multi_face_landmarks:
        return False

    # Extract landmarks for the first detected face
    landmarks = results.multi_face_landmarks[0]
    face_points = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in landmarks.landmark]

    if prev_landmarks is None:
        prev_landmarks = face_points
        return False  # No motion detected on first frame

    # Calculate total movement by summing Euclidean distances between corresponding points
    total_motion = sum(
        math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        for (x1, y1), (x2, y2) in zip(prev_landmarks, face_points)
    )
    prev_landmarks = face_points 

    # Store motion history
    motion_score_history.append(total_motion)
    if len(motion_score_history) > motion_window:
        motion_score_history.pop(0)

    # Use rolling average for stability
    avg_motion = np.mean(motion_score_history)

    motion_detected_flag = avg_motion > motion_threshold
    return motion_detected_flag

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
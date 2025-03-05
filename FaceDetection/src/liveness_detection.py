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
MODEL_PATH = os.path.join(BASE_DIR, "../models/n_version2_10best.pt")
model = YOLO(MODEL_PATH)
classNames = ["fake", "real"]

confidence=0.8
# Motion detection variables
prev_frame = None
motion_threshold = 1500
blink_threshold = 0.2  # Tune this for eye blink detection
blink_counter = 0


def detect_motion(frame):
    """Detects motion by comparing the current frame with the previous frame."""
    global prev_frame, blink_counter

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # Reduce noise

    if prev_frame is None:
        prev_frame = gray
        return False, False  # No motion detected in the first frame

    # Compute the absolute difference between the current frame and previous frame
    frame_diff = cv2.absdiff(prev_frame, gray)
    prev_frame = gray  # Update previous frame

    # Apply thresholding
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    motion_score = np.sum(thresh)  # Calculate motion intensity

    motion_detected = motion_score > motion_threshold

    # Detect face landmarks using Mediapipe
    blink_detected = False
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract eye landmarks
            left_eye = [face_landmarks.landmark[i] for i in [33, 160, 158, 133, 153, 144]]
            right_eye = [face_landmarks.landmark[i] for i in [362, 385, 387, 263, 373, 380]]

            # Compute eye aspect ratio (EAR) to detect blinking
            def eye_aspect_ratio(eye):
                A = math.dist((eye[1].x, eye[1].y), (eye[5].x, eye[5].y))
                B = math.dist((eye[2].x, eye[2].y), (eye[4].x, eye[4].y))
                C = math.dist((eye[0].x, eye[0].y), (eye[3].x, eye[3].y))
                return (A + B) / (2.0 * C)

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0
            print(f"Left EAR: {left_ear}, Right EAR: {right_ear}, Avg EAR: {avg_ear}")


            if avg_ear < blink_threshold:  # Eyes are closed
                blink_counter += 1
            else:
                if blink_counter > 2:  # If blink detected
                    blink_detected = True
                blink_counter = 0  # Reset counter

    return motion_detected, blink_detected

def identify_real_or_fake(frame):
    motion_detected, blink_detected = detect_motion(frame)
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
                    if motion_detected and blink_detected:
                        identification = 'fake'  # Only mark as fake if neither movement nor blinking is detected
                    else:
                        identification = 'real'  # If any one is detected, keep it real

                color = (0, 255, 0) if identification == 'real' else (0, 0, 255)
                cvzone.cornerRect(frame, (x1, y1, w, h), colorC=color, colorR=color)
                cvzone.putTextRect(frame, f'{identification.upper()} {int(conf*100)}%',
                                   (max(0, x1), max(35, y1)), scale=2, thickness=4, colorR=color,
                                   colorB=color)
                return identification  # Return "real" or "fake"
    
    return None  # Return None if no valid prediction is made
import cv2
import time
from flask import Response
from src.utils.liveness_detection import identify_real_or_fake
from config.config import CAM_WIDTH, CAM_HEIGHT

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    while True:
        success, frame = cap.read()
        if not success:
            break

        spoofing_test = identify_real_or_fake(frame)  # Perform liveness detection

        # Encode frame for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


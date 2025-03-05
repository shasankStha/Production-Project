import math
import time

import cv2
import cvzone
from ultralytics import YOLO
from src.liveness_detection import identify_real_or_fake

#################################
confidence = 0.8
camWidth, camHeight = 640, 480
#################################

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(3, camWidth)
    cap.set(4, camHeight)

    prev_frame_time = 0

    while True:
        new_frame_time = time.time()
        
        ret, frame = cap.read()
        if not ret:
            break

        result = identify_real_or_fake(frame)

        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        # print(f"FPS: {fps:.2f}")

        cv2.imshow("Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

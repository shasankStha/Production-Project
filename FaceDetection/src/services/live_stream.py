import cv2
import cvzone
import os
import joblib
from cvzone.FaceDetectionModule import FaceDetector
from src.utils.liveness_detection import identify_real_or_fake
from config.config import (
    CAM_WIDTH, CAM_HEIGHT, OFFSET_PERCENTAGE_W, OFFSET_PERCENTAGE_H, MODEL_PATH
)
detector = FaceDetector()

def identify_face(facearray):
    model = joblib.load(MODEL_PATH)
    return model.predict(facearray)[0]

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = FaceDetector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def generate_frames(attendance:False):
    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, CAM_WIDTH)
        cap.set(4, CAM_HEIGHT)
        if not cap.isOpened():
            raise Exception("Camera access failed.")

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame, bboxs = detector.findFaces(frame, draw=False)

            if len(bboxs) > 0:
                bbox = bboxs[0]
                x, y, w, h = bbox["bbox"]
                offsetW = (OFFSET_PERCENTAGE_W / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)
                offsetH = (OFFSET_PERCENTAGE_H / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)

                # Spoofing detection
                spoofing_test, conf = identify_real_or_fake(frame)

                if spoofing_test == 'fake' or spoofing_test == 'real':
                    color = (0, 255, 0) if spoofing_test == "real" else (0, 0, 255)
                    cv2.putText(frame, f"{spoofing_test.upper()} {int(conf * 100)}%", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                    cvzone.cornerRect(frame, (x, y, w, h), colorC=color, colorR=color)

                    # Attendance
                    if spoofing_test == 'real' and attendance:
                        face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                        face_array = face.reshape(1, -1)
                        identified_person = identify_face(face_array)
                        print(identified_person)


            _, buffer = cv2.imencode(".jpg", frame,[cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    except Exception as e:
        print(f"An error occurred in generate_frames: {str(e)}")
        yield b""

    finally:
        cap.release()
        cv2.destroyAllWindows()
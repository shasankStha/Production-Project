import cv2
import cvzone
import os
import joblib
import numpy as np
import torch
from threading import Lock
from facenet_pytorch import MTCNN, InceptionResnetV1
from cvzone.FaceDetectionModule import FaceDetector
from src.utils.liveness_detection import identify_real_or_fake
from src.utils.extensions import thread_pool
from config.config import (
    CAM_WIDTH, CAM_HEIGHT, OFFSET_PERCENTAGE_W, OFFSET_PERCENTAGE_H, MODEL_PATH,RECOGNITION_THRESHOLD, RECOGNITION_INTERVAL
)

# device = 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
embeddings = {} 

if os.path.exists(MODEL_PATH):
    data = joblib.load(MODEL_PATH)
    embeddings = data.get('embeddings', {})
    print(f"[INFO] Loaded {len(embeddings)} users from {MODEL_PATH}")

detector = FaceDetector()
last_identified_person = None
lock = Lock()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def identify_face(face_img):
    try:
        face = cv2.resize(face_img, (160, 160))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face_tensor = torch.tensor(face).permute(2, 0, 1).float().to(device)
        face_tensor = (face_tensor - 127.5) / 128.0
        
        with torch.no_grad():
            embedding = resnet(face_tensor.unsqueeze(0)).cpu().numpy().flatten()
        
        best_match = None
        highest_similarity = 0.0
        threshold = RECOGNITION_THRESHOLD
        
        for user, user_embedding in embeddings.items():
            similarity = cosine_similarity(embedding, user_embedding)
            if similarity > highest_similarity and similarity >= threshold:
                highest_similarity = similarity
                best_match = user
        
        return best_match
    except Exception as e:
        print(f"[ERROR] Identification failed: {str(e)}")
        return None

def generate_frames(attendance:False):
    global embeddings
    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, CAM_WIDTH)
        cap.set(4, CAM_HEIGHT)
        if not cap.isOpened():
            raise Exception("Camera access failed.")
        
        if attendance:
            data = joblib.load(MODEL_PATH)
            embeddings = data.get('embeddings', {})
        
        # Variables for frame skipping and storing results
        frame_counter = 0
        recognition_interval = RECOGNITION_INTERVAL

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
                face_roi = frame[y:y+h, x:x+w]
                if spoofing_test == 'fake' or spoofing_test == 'real':
                    color = (0, 255, 0) if spoofing_test == "real" else (0, 0, 255)
                    cv2.putText(frame, f"{spoofing_test.upper()} {int(conf * 100)}%", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                    cvzone.cornerRect(frame, (x, y, w, h), colorC=color, colorR=color)

                    # Attendance
                    if spoofing_test == 'real' and attendance:
                        if frame_counter % recognition_interval == 0:
                            def update_recognition():
                                global last_identified_person
                                identified = identify_face(face_roi)
                                with lock:
                                    last_identified_person = identified

                            thread_pool.submit(update_recognition)

                        with lock:
                            if last_identified_person:
                                text_size = cv2.getTextSize(last_identified_person, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                                text_x = x + (w - text_size[0]) // 2
                                text_y = y + h - 30
                                cv2.putText(frame, last_identified_person, (text_x, text_y),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            frame_counter += 1

            _, buffer = cv2.imencode(".jpg", frame,[cv2.IMWRITE_JPEG_QUALITY, 40])
            frame_bytes = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    except Exception as e:
        print(f"An error occurred in generate_frames: {str(e)}")
        yield b""

    finally:
        cap.release()
        cv2.destroyAllWindows()

import os
import cv2
import cvzone
import time
from cvzone.FaceDetectionModule import FaceDetector
from config.config import (
    CAM_WIDTH, CAM_HEIGHT, CONFIDENCE, BLUR_THRESHOLD, 
    NUMBER_OF_CAPTURE_IMAGE, OFFSET_PERCENTAGE_W, OFFSET_PERCENTAGE_H
)
from src.utils.liveness_detection import identify_real_or_fake

detector = FaceDetector()

def capture_face(user_name):
    """Captures face images while detecting liveness and sends instructions via WebSocket."""
    image_dir = os.path.join("images", user_name)
    os.makedirs(image_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    instructions = ["Look straight", "Look left", "Look right", "Look up", "Look down"]
    captured_images = 0
    batch_size = NUMBER_OF_CAPTURE_IMAGE // len(instructions)

    for instruction in instructions:
        print(instruction)
        time.sleep(1)

        for _ in range(batch_size):
            success, img = cap.read()
            if not success:
                print("[ERROR] Camera access failed.")
                break

            # Perform liveness detection
            spoofing_test, conf = identify_real_or_fake(img)

            img, bboxs = detector.findFaces(img, draw=True)
            if bboxs:
                for bbox in bboxs:
                    x, y, w, h = bbox["bbox"]

                    score = float(bbox["score"][0])
                    if score > CONFIDENCE:
                        if spoofing_test == "fake":
                            color = (0, 0, 255) 
                            cvzone.cornerRect(img, (x, y, w, h), colorC=color, colorR=color)
                            cvzone.putTextRect(img, f"FAKE {int(conf * 100)}%", (x, y - 10), scale=2, thickness=4, colorR=color)
                            continue

                        offsetW = (OFFSET_PERCENTAGE_W/100)*w
                        x = int(x - offsetW)
                        w = int(w + offsetW * 2)

                        offsetH = (OFFSET_PERCENTAGE_H/100)*h
                        y = int(y - offsetH * 3)
                        h = int(h + offsetH * 3.5)

                        if x < 0:x=0
                        if y < 0:y=0
                        if w < 0:w=0
                        if h < 0:h=0

                        face = img[y:y + h, x:x + w]
                        blur_value = int(cv2.Laplacian(face, cv2.CV_64F).var())
                        if blur_value > BLUR_THRESHOLD:
                            img_path = os.path.join(image_dir, f"{captured_images}.jpg")
                            cv2.imwrite(img_path, face)
                            captured_images += 1

            if cv2.waitKey(1) & 0xFF in [ord('q'), 27]: 
                cap.release()
                cv2.destroyAllWindows()
                return image_dir if captured_images >= NUMBER_OF_CAPTURE_IMAGE else None

    cap.release()
    cv2.destroyAllWindows()
    return image_dir if captured_images >= NUMBER_OF_CAPTURE_IMAGE else None

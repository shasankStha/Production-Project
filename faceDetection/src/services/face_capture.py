import os
import cv2
import cvzone
import time
from cvzone.FaceDetectionModule import FaceDetector
from config.config import (
    CAM_WIDTH, CAM_HEIGHT, LIVENESS_CONFIDENCE, BLUR_THRESHOLD,
    NUMBER_OF_CAPTURE_IMAGE, OFFSET_PERCENTAGE_W, OFFSET_PERCENTAGE_H,
    IMAGE_DIR
)
from src.utils.liveness_detection import identify_real_or_fake

detector = FaceDetector()

def capture_face(user_identification):
    """Captures face images while detecting liveness."""
    image_dir = os.path.join(IMAGE_DIR, user_identification)
    try:
        os.makedirs(image_dir, exist_ok=True)
    except Exception as e:
        print(f" Failed to create image directory: {str(e)}")
        return None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera access failed.")
        return None

    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    captured_images = 0
    total_images = NUMBER_OF_CAPTURE_IMAGE

    try:
        while captured_images < total_images:
            success, img = cap.read()
            if not success:
                print("Failed to capture image from camera.")
                break

            spoofing_test, conf = identify_real_or_fake(img)
            img, bboxs = detector.findFaces(img, draw=False)

            if bboxs:
                for bbox in bboxs:
                    x, y, w, h = bbox["bbox"]
                    score = float(bbox["score"][0])

                    if score > LIVENESS_CONFIDENCE:
                        if spoofing_test == "fake":
                            color = (0, 0, 255)
                            cvzone.cornerRect(img, (x, y, w, h), colorC=color, colorR=color)
                            cvzone.putTextRect(img, f"FAKE {int(conf * 100)}%", (x, y - 10), scale=2, thickness=4, colorR=color)
                            continue

                        offsetW = (OFFSET_PERCENTAGE_W / 100) * w
                        x = int(x - offsetW)
                        w = int(w + offsetW * 2)
                        offsetH = (OFFSET_PERCENTAGE_H / 100) * h
                        y = int(y - offsetH * 3)
                        h = int(h + offsetH * 3.5)

                        x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)
                        face = img[y:y + h, x:x + w]
                        blur_value = int(cv2.Laplacian(face, cv2.CV_64F).var())

                        if blur_value > BLUR_THRESHOLD:
                            img_path = os.path.join(image_dir, f"{captured_images}.jpg")
                            try:
                                cv2.imwrite(img_path, face)
                                captured_images += 1
                                if captured_images % 25 == 0:
                                    time.sleep(1)
                            except Exception as e:
                                print(f"Failed to save image: {str(e)}")

        return image_dir if captured_images >= total_images else None

    except Exception as e:
        print(f"An error occurred during face capture: {str(e)}")
        return None

    finally:
        cap.release()
        cv2.destroyAllWindows()
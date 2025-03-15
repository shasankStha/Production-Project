import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from src.utils.liveness_detection import identify_real_or_fake

detector = FaceDetector()  

def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame, bboxs = detector.findFaces(frame, draw=False)

        if len(bboxs) > 0:
            bbox = bboxs[0]
            x, y, w, h = bbox["bbox"]

            spoofing_test, conf = identify_real_or_fake(frame)


            # if spoofing_test == 'fake':
            #     cvzone.cornerRect(frame, (x, y, w, h), colorC=color, colorR=color)

            if spoofing_test == 'fake' or spoofing_test == 'real':
                color = (0, 255, 0) if spoofing_test == "real" else (0, 0, 255)
                cvzone.cornerRect(frame, (x, y, w, h), colorC=color, colorR=color)

                cv2.putText(frame, f"{spoofing_test.upper()} {int(conf * 100)}%", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    cap.release()

# import math
# import time

# import cv2
# import cvzone
# from ultralytics import YOLO
# from src.liveness_detection import identify_real_or_fake

# #################################
# confidence = 0.8
# camWidth, camHeight = 1280, 720
# #################################

# def main():
    
#     cap = cv2.VideoCapture(0)
#     cap.set(3, camWidth)
#     cap.set(4, camHeight)

#     prev_frame_time = 0

#     while True:
#         new_frame_time = time.time()
        
#         ret, frame = cap.read()
#         if not ret:
#             break

#         result = identify_real_or_fake(frame)

#         fps = 1 / (new_frame_time - prev_frame_time)
#         prev_frame_time = new_frame_time
#         # print(f"FPS: {fps:.2f}")

#         cv2.imshow("Video Feed", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


from flask import Flask, render_template, Response
import cv2
import math
import time
from cvzone.FaceDetectionModule import FaceDetector
from ultralytics import YOLO
from src.liveness_detection import identify_real_or_fake

#################################
confidence = 0.8
camWidth, camHeight = 1280, 720
#################################

app = Flask(__name__)

face_detector = FaceDetector()

# Function to capture video frames and detect faces
def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, camWidth)
    cap.set(4, camHeight)

    prev_frame_time = 0
    
    while True:
        new_frame_time = time.time()
        img, frame = cap.read()
        if not img:
            break
        else:
            frame, faces = face_detector.findFaces(frame, draw=False)
            # for face in faces:
            #     x1, y1, w, h = face['bbox']
            #     spoofing_test, conf = identify_real_or_fake(frame[y1:y1+h, x1:x1+w])
            #     color = (0, 255, 0) if spoofing_test == 'real' else (0, 0, 255)
                
            #     cvzone.cornerRect(frame, (x1, y1, w, h), colorC=color, colorR=color)
            #     cvzone.putTextRect(frame, f'{spoofing_test.upper()} {int(conf*100)}%',
            #                         (max(0, x1), max(35, y1)), scale=2, thickness=4, colorR=color,
            #                         colorB=color)
            spoofing_test = identify_real_or_fake(frame)
            
            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML page

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)


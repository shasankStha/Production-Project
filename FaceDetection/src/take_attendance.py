import os
import csv
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from datetime import datetime
import face_recognition
from .liveness_detection import identify_real_or_fake

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
attendance_file = os.path.join(BASE_DIR, "../images")
image_dir = os.path.join(BASE_DIR, "../attendance/attendance.csv")
confidence_threshold = 0.8

# Initialize face detector
detector = FaceDetector()

def load_registered_faces():
    """Loads registered users' face encodings from stored images."""
    known_face_encodings = []
    known_face_names = []
    
    for user in os.listdir(image_dir):
        user_path = os.path.join(image_dir, user)
        if os.path.isdir(user_path):
            for img_name in os.listdir(user_path):
                img_path = os.path.join(user_path, img_name)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(user)
    
    return known_face_encodings, known_face_names

def mark_attendance(name):
    """Marks attendance in the CSV file."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(attendance_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, timestamp])
    
    print(f"[INFO] Attendance marked for {name} at {timestamp}")

def take_attendance():
    """Captures video stream, detects faces, verifies liveness, and marks attendance."""
    known_face_encodings, known_face_names = load_registered_faces()
    cap = cv2.VideoCapture(0)
    print("[INFO] Taking attendance...")
    
    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Unable to access camera.")
            break
        
        img, bboxs = detector.findFaces(img, draw=True)
        user = None
        
        if bboxs:
            for bbox in bboxs:
                x, y, w, h = bbox["bbox"]
                score = float(bbox["score"][0])
                if score > confidence_threshold:
                    face_frame = img[y:y+h, x:x+w]
                    
                    # Liveness Detection
                    identification = identify_real_or_fake(img)
                    if identification != "real":
                        print("[ALERT] Fake face detected! Ignoring...")
                        continue
                    
                    # Face Recognition
                    face_encoding = face_recognition.face_encodings(img, [(y, x+w, y+h, x)])
                    if face_encoding:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding[0])
                        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None
                        
                        if best_match_index is not None and matches[best_match_index]:
                            user = known_face_names[best_match_index]
                            mark_attendance(user)

            cv2.rectangle(img, (x,y,w,h), (255,0,0), 3)
            cvzone.putTextRect(img, f'{user!="None": user}',(x,y-0), scale=2, thickness= 3)
                
        cv2.imshow("Attendance System", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_attendance()

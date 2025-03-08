import os
import csv
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from time import time

camWidth, camHeight = 640, 480
blurThreshold = 70
confidence = 0.8
offsetPercentageW = 10
offsetPercentageH = 20

numberOfCaptureImage = 100


def capture_face(name):
    """Captures the user's face using face detection and saves images to the images/{username} directory."""
    image_dir = os.path.join("images", name)
    os.makedirs(image_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    cap.set(3,camWidth)
    cap.set(4,camHeight)
    detector = FaceDetector()

    captured_images = 0
    
    while captured_images < numberOfCaptureImage:
        success, img = cap.read()
        if not success:
            print("[ERROR] Unable to access camera.")
            break
        
        img, bboxs = detector.findFaces(img, draw=False)
        if bboxs:
            for bbox in bboxs:
                x, y, w, h = bbox["bbox"]
                score = float(bbox["score"][0])
                # Check score
                if score > confidence:
                    # Adding Offset to the face Detected
                    offsetW = (offsetPercentageW/100)*w
                    x = int(x - offsetW)
                    w = int(w + offsetW * 2)

                    offsetH = (offsetPercentageH/100)*h
                    y = int(y - offsetH * 3)
                    h = int(h + offsetH * 3.5)

                    # To avoid values below 0
                    if x < 0:x=0
                    if y < 0:y=0
                    if w < 0:w=0
                    if h < 0:h=0

                    # Find Blurriness
                    face = img[y:y+h, x:x+w]
                    blur_value = int(cv2.Laplacian(face, cv2.CV_64F).var())
                    
                    if blur_value > blurThreshold:  # Ensure the face is in focus
                        image_path = os.path.join(image_dir, f"{captured_images}.jpg")
                        cv2.imwrite(image_path, face)
                        captured_images += 1

                cv2.rectangle(img, (x,y,w,h), (255,0,0), 3)
                cvzone.putTextRect(img, f'Score: {int(score*100)}% Blur: {blur_value}',(x,y-0), scale=2, thickness= 3)
        
        cv2.imshow("Capture Face", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  
    return image_dir if captured_images >= numberOfCaptureImage else None

def add_user():
    csv_file = "users.csv"
    
    # Ensure CSV file exists with headers
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Name", "Email", "Image Path"])
    
    user_id = input("Enter User ID: ")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    
    image_path = capture_face(name)
    
    if image_path:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, name, email, image_path])
        print(f"User {name} added successfully with face data!")
    else:
        print("[ERROR] Face capture failed. User not added.")
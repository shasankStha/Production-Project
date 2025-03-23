import os

# Camera settings
CAM_WIDTH = 1280
CAM_HEIGHT = 720
BLUR_THRESHOLD = 40
NUMBER_OF_CAPTURE_IMAGE = 100
OFFSET_PERCENTAGE_W = 10
OFFSET_PERCENTAGE_H = 20

# Directories
IMAGE_DIR = "static/"
MODEL_PATH = "models/face_recognition_model.pkl"
CSV_FILE = os.path.join("database", "users.csv")

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        import csv
        writer = csv.writer(file)
        writer.writerow(["User ID", "Name", "Email", "Image Path"])

#Liveness Detection
LIVENESS_DETECTION_MODEL = "models/n_version4_10best.pt"
CLASSNAMES = ["fake", "real"]
LIVENESS_CONFIDENCE = 0.8

# Recognition
RECOGNITION_INTERVAL = 4 #No of frames
RECOGNITION_THRESHOLD = 0.6

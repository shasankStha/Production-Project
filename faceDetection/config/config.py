import os
from dotenv import load_dotenv
import joblib

load_dotenv()

# Camera settings
CAM_WIDTH = 1280
CAM_HEIGHT = 720
BLUR_THRESHOLD = 40
NUMBER_OF_CAPTURE_IMAGE = 100
OFFSET_PERCENTAGE_W = 10
OFFSET_PERCENTAGE_H = 20

# Directories
IMAGE_DIR = "static/"
MODEL_PATH = "trained_models/face_recognition_model.pkl"
CSV_FILE = os.path.join("database", "users.csv")

# Ensure model exists
if not os.path.isfile(MODEL_PATH):
    initial_model = {"embeddings": {}}
    joblib.dump(initial_model, MODEL_PATH)

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        import csv
        writer = csv.writer(file)
        writer.writerow(["User ID", "Name", "Email", "Image Path"])

##Image Quality For Live Streaming
IMG_JPEG_QUALITY = 50

#Liveness Detection
LIVENESS_DETECTION_MODEL = "trained_models/n_version4_10best.pt"
CLASSNAMES = ["fake", "real"]
LIVENESS_CONFIDENCE = 0.8

# Recognition
RECOGNITION_INTERVAL = 4 #No of frames
RECOGNITION_THRESHOLD = 0.6
RECOGITION_TIMEOUT = 2 #No of sec to be inserted in database

# Database
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


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

# Ensure model exists
if not os.path.isfile(MODEL_PATH):
    initial_model = {"embeddings": {}}
    joblib.dump(initial_model, MODEL_PATH)

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)

##Image Quality For Live Streaming
IMG_JPEG_QUALITY = 50

#Liveness Detection
LIVENESS_DETECTION_MODEL = "trained_models/n_version4_10best.pt"
CLASSNAMES = ["fake", "real"]
LIVENESS_CONFIDENCE = 0.8

# Recognition
RECOGNITION_INTERVAL = 2 #No of frames
RECOGNITION_THRESHOLD = 0.75
RECOGITION_TIMEOUT = 2 #No of sec to be inserted in database

SCHEDULE_HOUR = 21  # Example: 11 PM
SCHEDULE_MINUTE = 45  # Example: 59 minutes past the hour


#Database
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("ADMIN_EMAIL")
    MAIL_PASSWORD = os.getenv("ADMIN_PASSWORD")  
    MAIL_DEFAULT_SENDER = os.getenv("ADMIN_EMAIL")

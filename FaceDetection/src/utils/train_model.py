import os
import face_recognition
import joblib
from config.config import IMAGE_DIR

MODEL_PATH = "models/face_recognition_model.pkl"

def train_model(user_identifier, image_dir):
    try:
        known_encodings = []
        known_names = []

        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                data = joblib.load(f)
                known_encodings = data["encodings"]
                known_names = data["names"]

        for img_name in os.listdir(image_dir):
            img_path = os.path.join(image_dir, img_name)
            img = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(img)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(user_identifier)

        data = {"encodings": known_encodings, "names": known_names}
        with open(MODEL_PATH, "wb") as f:
            joblib.dump(data, f)

        print("[INFO] Model trained successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] An error occurred during model training: {str(e)}")
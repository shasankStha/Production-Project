import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

IMG_SIZE = 64

def load_model_with_path(path):
    return load_model(path)

def detect_liveness(frame, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    if len(faces) == 0:
        return None, None

    x, y, w, h = faces[0]  # Consider the first detected face
    face = frame[y:y+h, x:x+w]
    face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
    face_resized = np.expand_dims(face_resized, axis=0) / 255.0  # Normalize

    # Predict using the model
    prediction = model.predict(face_resized)[0][0]
    label = "Real" if prediction > 0.5 else "Fake"

    return label, (x, y, w, h)

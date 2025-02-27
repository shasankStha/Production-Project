import face_recognition
import os
import numpy as np
import pickle
import cv2

ENCODINGS_FILE = "models/face_encodings.pkl"

def load_known_faces():
    if not os.path.exists(ENCODINGS_FILE):
        return [], []

    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data["encodings"], data["names"]

def recognize_face(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            return known_names[match_index]
    
    return None

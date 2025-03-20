import os
import numpy as np
import cv2
import joblib
from sklearn.neighbors import KNeighborsClassifier
from config.config import MODEL_PATH

def train_model(user_name, image_dir):
    print(user_name, image_dir)
    faces = []
    labels = []
    try:
        if os.path.exists(MODEL_PATH):
            knn = joblib.load(MODEL_PATH)
            faces = knn._fit_X.tolist()
            labels = knn.classes_.tolist()
        
        userlist = os.listdir(image_dir)
        for user in userlist:
            user_dir = os.path.join(image_dir, user)
            
            if not os.path.isdir(user_dir):
                continue

            for imgname in os.listdir(user_dir):
                img_path = os.path.join(user_dir, imgname)
                img = cv2.imread(img_path)
            
                if img is None:
                    print(f"Unable to read image: {img_path}")
                    continue
            
                resized_face = cv2.resize(img, (50, 50))
                faces.append(resized_face.ravel())
                labels.append(user_name)

        if len(faces) == 0:
            print("[ERROR] No valid face images found for training.")
            return False
        
        faces = np.array(faces)
        labels = np.array(labels)

        print("[INFO] Training/updating the KNN model...")
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, labels)

        # Save the updated model
        joblib.dump(knn, MODEL_PATH)
        print("[INFO] Model trained and saved successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] An error occurred during model training: {str(e)}")
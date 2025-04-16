import os
import numpy as np
import cv2
import joblib
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from sklearn.preprocessing import normalize
from config.config import MODEL_PATH

# Initialize FaceNet model and face detector
# device = 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def get_embedding(face_image):
    """Generate 512-dimensional embedding from face image"""
    try:
        face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (160, 160)) 
        face_tensor = torch.tensor(face).permute(2, 0, 1).float().to(device)
        face_tensor = (face_tensor - 127.5) / 128.0
        with torch.no_grad():
            embedding = resnet(face_tensor.unsqueeze(0)).cpu().numpy().flatten()
        return normalize(embedding.reshape(1, -1)).flatten()
    except Exception as e:
        print(f"[ERROR] Embedding failed: {str(e)}")
        return None

def train_model(user_name, image_dir):
    try:
        if os.path.exists(MODEL_PATH):
            data = joblib.load(MODEL_PATH)
            embeddings = data.get('embeddings', {})
        else:
            embeddings = {}

        user_embeddings = []
        for image_file in os.listdir(image_dir):
            img_path = os.path.join(image_dir, image_file)
            img = cv2.imread(img_path)
            
            if img is None:
                print(f"Unable to read image: {img_path}")
                continue

            boxes, _ = mtcnn.detect(img)
            if boxes is None:
                print(f"[WARNING] No face detected in {img_path}")
                continue

            x1, y1, x2, y2 = boxes[0].astype(int)
            face = img[y1:y2, x1:x2]
            
            embedding = get_embedding(face)
            if embedding is None:
                continue
            user_embeddings.append(embedding)

        if not user_embeddings:
            print("[ERROR] No valid faces found for training")
            return False

        avg_embedding = np.mean(user_embeddings, axis=0)
        avg_embedding = normalize(avg_embedding.reshape(1, -1)).flatten()

        embeddings[user_name] = avg_embedding
        joblib.dump({'embeddings': embeddings}, MODEL_PATH)
        print(f"[INFO] User '{user_name}' registered successfully")
        return True

    except Exception as e:
        print(f"[ERROR] Training failed: {str(e)}")
        return False
    
def remove_user_from_model(user_name):
    try:
        if not os.path.exists(MODEL_PATH):
            print("[INFO] Model file does not exist.")
            return

        data = joblib.load(MODEL_PATH)
        embeddings = data.get('embeddings', {})

        if user_name in embeddings:
            del embeddings[user_name]
            joblib.dump({'embeddings': embeddings}, MODEL_PATH)
            print(f"[INFO] User '{user_name}' removed from model.")
        else:
            print(f"[INFO] User '{user_name}' not found in model.")

    except Exception as e:
        print(f"[ERROR] Failed to remove user: {str(e)}")


def rename_user_in_model(old_name, new_name):
    try:
        if not os.path.exists(MODEL_PATH):
            print("[INFO] Model file does not exist.")
            return

        data = joblib.load(MODEL_PATH)
        embeddings = data.get('embeddings', {})

        if old_name not in embeddings:
            print(f"[INFO] User '{old_name}' not found in model.")
            return

        embeddings[new_name] = embeddings.pop(old_name)
        joblib.dump({'embeddings': embeddings}, MODEL_PATH)
        print(f"[INFO] Renamed '{old_name}' to '{new_name}' in model.")

    except Exception as e:
        print(f"[ERROR] Failed to rename user: {str(e)}")

import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Set paths
MODEL_PATH = "models/liveness_model.h5"
DATASET_PATH = "processed_dataset"
IMG_SIZE = 64  

# Define real and fake categories
REAL_CATEGORIES = ["real","live_selfie","live_video"]
FAKE_CATEGORIES = ["mask", "monitor", "outline", "print", "print_cut", "silicone","cut-out printouts","printouts","replay"]

def load_images(category, label):
    images, labels = [], []
    folder_path = os.path.join(DATASET_PATH, category)

    if not os.path.exists(folder_path):
        return images, labels

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
            labels.append(label)

    return images, labels

def train_model():
    if os.path.exists(MODEL_PATH):
        print("✅ Model already exists. Skipping training.")
        return

    print("⚡ Training model...")
    
    # Load real images
    real_images, real_labels = [], []
    for category in REAL_CATEGORIES:
        imgs, lbls = load_images(category, "real")
        real_images.extend(imgs)
        real_labels.extend(lbls)
    
    # Load fake images
    fake_images, fake_labels = [], []
    for category in FAKE_CATEGORIES:
        imgs, lbls = load_images(category, "fake")
        fake_images.extend(imgs)
        fake_labels.extend(lbls)

    X = np.array(real_images + fake_images) / 255.0  # Normalize
    y = np.array(real_labels + fake_labels)

    if len(X) == 0:
        print("⚠️ No training data found. Skipping model training.")
        return

    # Encode labels (real -> 1, fake -> 0)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Dataset loaded: {len(X_train)} training images, {len(X_test)} testing images")

    # Build CNN model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid') 
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=16)
    
    # Save the model
    model.save(MODEL_PATH)
    print("✅ Model training complete. Saved at:", MODEL_PATH)

if __name__ == "__main__":
    train_model()

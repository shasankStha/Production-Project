import os
from src.extract_frames import extract_frames
from src.train_model import train_model
from src.liveness_detection import load_model_with_path, detect_liveness
import cv2

MODEL_PATH = "models/liveness_model.h5"

def main():
    print("⚡ Checking dataset and model...")

    # Extract frames if processed dataset is missing
    if not os.path.exists("processed_dataset"):
        extract_frames()

    # Train model only if not found
    if not os.path.exists(MODEL_PATH):
        train_model()

    print("✅ Model loaded. Running real-time liveness detection...")
    model = load_model_with_path(MODEL_PATH)  # Load trained model
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        label, bbox = detect_liveness(frame, model)
        if label:
            x, y, w, h = bbox
            color = (0, 255, 0) if label == "Real" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Liveness Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2
import os

VIDEO_FOLDER = "archive/files"
OUTPUT_FOLDER = "processed_dataset"

def extract_frames():
    if os.path.exists(OUTPUT_FOLDER):
        print("✅ Extracted frames already exist. Skipping extraction.")
        return

    print("⚡ Extracting frames from videos...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for category in os.listdir(VIDEO_FOLDER):
        category_path = os.path.join(VIDEO_FOLDER, category)
        output_category_path = os.path.join(OUTPUT_FOLDER, category)
        os.makedirs(output_category_path, exist_ok=True)

        for video_file in os.listdir(category_path):
            video_path = os.path.join(category_path, video_file)
            cap = cv2.VideoCapture(video_path)
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_path = os.path.join(output_category_path, f"{video_file}_frame_{count}.jpg")
                cv2.imwrite(frame_path, frame)
                count += 1

            cap.release()

    print("✅ Frames extracted and stored in", OUTPUT_FOLDER)

if __name__ == "__main__":
    extract_frames()

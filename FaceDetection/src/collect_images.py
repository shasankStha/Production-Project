import cv2
import os

def collect_images(output_folder="dataset", num_images=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break

        img_path = os.path.join(output_folder, f"image_{count}.jpg")
        cv2.imwrite(img_path, frame)
        count += 1

        cv2.imshow("Collecting Images", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Collected {count} images in {output_folder}")

if __name__ == "__main__":
    collect_images()

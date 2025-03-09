import math
import time

import cv2
import cvzone
from ultralytics import YOLO
from src.liveness_detection import identify_real_or_fake

#################################
confidence = 0.8
camWidth, camHeight = 1280, 720
#################################

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(3, camWidth)
    cap.set(4, camHeight)

    prev_frame_time = 0

    while True:
        new_frame_time = time.time()
        
        ret, frame = cap.read()
        if not ret:
            break

        result = identify_real_or_fake(frame)

        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        # print(f"FPS: {fps:.2f}")

        cv2.imshow("Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
# import time
# from src.add_user import add_user
# from src.take_attendance import take_attendance

# def main():
#     while True:
#         print("\nFace Recognition Attendance System")
#         print("1. Add User")
#         print("2. Take Attendance")
#         print("3. Exit")
#         choice = input("Enter your choice: ")

#         if choice == '1':
#             add_user()
#         elif choice == '2':
#             take_attendance()
#         elif choice == '3':
#             print("Exiting...\n")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main()
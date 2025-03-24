# Liveness Detection Module

This module implements robust liveness detection for an attendance recording system by combining computer vision techniques with deep learning. It ensures that only live individuals are recorded, mitigating spoofing attempts (e.g., using photos or video replays). The liveness detection mechanism is based on three complementary techniques:

1. **Facial Landmark-Based Motion Detection**
2. **Proximity (Face Distance) Check**
3. **Deep Learning-Based Classification (YOLO Model)**

Each component adds a layer of security to ensure the authenticity of the face being captured.

## Detailed Mechanism

### 1. Facial Landmark-Based Motion Detection

- **How It Works:**

  - **Facial Landmark Extraction:**  
    Utilizes Mediapipe's Face Mesh to extract 468 facial landmarks from the input video frame.
  - **Motion Calculation:**  
    The script computes the Euclidean distance between corresponding landmarks from consecutive frames. These distances are summed to produce a “total motion” score.
  - **Average:**  
    A rolling average over a window of 10 frames is calculated to smooth out transient fluctuations. If the average motion exceeds a set threshold (3.0 pixels), it confirms that natural face movement is present.

- **Robustness:**
  - **Noise Reduction:**  
    The rolling average approach helps filter out noise or brief still periods.
  - **Liveness Verification:**  
    Natural, subtle movements of a live face (even when barely noticeable) are distinguished from the static nature of a spoof (like a photograph).

### 2. Proximity (Face Distance) Check

- **How It Works:**
  - **Distance Measurement:**  
    The distance between key facial landmarks (the left and right eyes) is used to estimate the face width.
  - **Threshold Check:**  
    If the measured face width exceeds a threshold (300 pixels), the system flags the face as too close to the camera and aborts further processing.
- **Robustness:**
  - **Anti-Spoofing:**  
    Prevents spoofing attempts by rejecting faces presented at an unnaturally close distance (a common trait in spoofing scenarios using photographs or screens).

### 3. Deep Learning-Based Classification (YOLO Model)

- **How It Works:**

  - **Model Integration:**  
    A YOLO model trained using own dataset and yolov8n classifies the input face as either "real" or "fake".
  - **Confidence Threshold:**  
    Only predictions with confidence above 0.8 are considered. This helps ensure that the decision is based on reliable model output.
  - **Decision Override:**  
    Even if the YOLO model predicts "real," if the motion detection indicates insufficient movement, the system overrides the prediction to "fake".

- **Robustness:**
  - **Multi-Layered Verification:**  
    Combining deep learning with real-time motion and proximity checks adds redundancy. An attacker would have to defeat all three measures simultaneously to spoof the system.
  - **Adaptability:**  
    The system is designed to work with typical webcam frame rates (10–14 FPS), ensuring real-time performance even under variable conditions.

## Practical Considerations for Attendance Systems

- **Security Against Spoofing:**  
  By using multiple verification methods (motion, proximity, and YOLO classification), the system robustly rejects static images, video replays, or any manipulated input.
- **Adaptability to Environment:**

  - **Thresholds are Tunable:**  
    Parameters like `motion_threshold`, `FACE_TOO_CLOSE_THRESHOLD`, and the confidence level can be adjusted based on the specific deployment environment and camera setup.
  - **Handling Variable Frame Rates:**  
    The motion detection mechanism’s rolling average adapts to different frame rates, ensuring consistent performance even if the FPS fluctuates.

- **User Experience:**
  - **Real-Time Feedback:**  
    The system provides immediate visual feedback (using cvzone overlays) that helps users adjust their positioning if the face is too close or if insufficient motion is detected.
  - **Balanced Sensitivity:**  
    The combination of deep learning and classical computer vision techniques ensures that legitimate users are not falsely rejected due to transient stillness, while still preventing spoofing attempts.

## Conclusion

This liveness detection module is a robust, multi-layered solution specifically designed for attendance recording systems. By integrating facial landmark-based motion detection, proximity checks, and deep learning-based classification, the system effectively differentiates between a live face and spoofing attempts. Its design ensures high security and adaptability, making it a concrete choice for reliable attendance verification.

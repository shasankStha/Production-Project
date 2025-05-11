# Facial Recognition Attendance System with Liveness Detection & Blockchain

A secure, real-time attendance system that uses facial recognition, advanced liveness detection, and blockchain technology to ensure tamper-proof and spoof-resistant attendance tracking.

---

## Features

- Real-Time Face Detection and Recognition
- Multi-layered **Liveness Detection**
- Immutable **Blockchain-based** attendance logging
- Decentralized image storage using **IPFS**
- **Admin Dashboard** with charts and calendar view
- Attendance **Search and Filtering**
- **JWT Authentication** for secure login

---

## Technologies Used

| Feature                | Technology / Tool                      |
| ---------------------- | -------------------------------------- |
| Frontend               | React, Tailwind CSS, Chart.js          |
| Backend                | Flask, PostgreSQL, JWT                 |
| Face Detection         | Ultralytics YOLOv8, MediaPipe, FaceNet |
| Liveness Detection     | Motion detection, YOLO, Proximity      |
| Blockchain Integration | Ethereum (Ganache, Web3.py)            |
| Decentralized Storage  | IPFS (via Pinata)                      |

---

## Liveness Detection Module

This module implements robust liveness detection for an attendance recording system by combining computer vision techniques with deep learning. It ensures that only live individuals are recorded, mitigating spoofing attempts (e.g., using photos or video replays). The liveness detection mechanism is based on three complementary techniques:

1. **Facial Landmark-Based Motion Detection**
2. **Proximity (Face Distance) Check**
3. **Deep Learning-Based Classification (YOLO Model)**

Each component adds a layer of security to ensure the authenticity of the face being captured.

### 1. Facial Landmark-Based Motion Detection

- **How It Works:**

  - Utilizes Mediapipe's Face Mesh to extract 468 facial landmarks.
  - Calculates Euclidean distance between corresponding landmarks across frames.
  - Applies a rolling average over 10 frames to confirm natural face movement.

- **Robustness:**
  - Filters out noise and false motion.
  - Detects subtle live facial movements unlike static spoofs.

### 2. Proximity (Face Distance) Check

- **How It Works:**

  - Estimates face width using eye landmarks.
  - Rejects frames where the face is too close (e.g., >300px width).

- **Robustness:**
  - Prevents spoofing with photos/screens held close to the camera.

### 3. Deep Learning-Based Classification (YOLO Model)

- **How It Works:**

  - A YOLOv8n model classifies faces as "real" or "fake".
  - Uses a confidence threshold (>0.8) to accept only reliable detections.
  - Motion override: If no real movement, label is changed to "fake" even if YOLO predicts "real".

- **Robustness:**
  - Multi-layered defense makes spoofing extremely difficult.
  - Designed for real-time use (10–14 FPS camera performance).

### Practical Considerations

- **Security:** Blocks static images, replays, and manipulated inputs.
- **Adaptability:** Thresholds (motion, distance, confidence) are configurable.
- **User Experience:** Real-time feedback via visual overlays helps users align correctly without errors.

---

---

## Admin Dashboard

The admin dashboard offers the following views:

- **Line Chart:** Weekly attendance trend.
- **Bar Chart:** Top 5 users by attendance.
- **Pie Chart:** Day-wise attendance distribution.
- **Calendar View:** Select and view attendance by date.
- **Search/Filter:** Lookup records based on user or date.

---

## 🔗 Blockchain & IPFS Integration

### 🧬 IPFS (InterPlanetary File System)

- **Local IPFS Node:**  
  The system uses a **locally hosted IPFS node** to store attendance records in a decentralized way.
- **What is Stored:**  
  Attendance data (e.g., timestamp, user ID, session info) is serialized and stored as a JSON object in IPFS.
- **Why Use IPFS:**  
  Ensures the data is stored in a **distributed, tamper-resistant** format, decoupling data from centralized storage systems.

### ⛓ Blockchain Integration

- After storing attendance data in IPFS, the returned **CID (Content Identifier)** is saved on the **Ethereum blockchain**.
- This creates an **immutable on-chain reference** to the off-chain data stored in IPFS.
- Guarantees **tamper-proof auditability** and ensures that attendance logs cannot be altered retroactively.
- Implemented using **Web3.py** and tested with **Ganache** (for local development).

---

## Authentication

- User and admin authentication is handled via **JWT (Flask-JWT-Extended)**.
- Secure session handling with token-based auth.
- Role-based access (admin vs user).

---

## Setup & Installation

### Prerequisites

- Python 3.10.9
- Node.js & npm
- Postgres
- IPFS
- Ganache

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

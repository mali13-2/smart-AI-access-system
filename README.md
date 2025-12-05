# smart-AI-access-system
An AI-powered dual authentication access control system combining RFID verification and DeepFace-based facial recognition with an Arduino-controlled stepper motor. This hybrid system ensures secure, real-time, and intelligent physical access using both hardware validation and AI-driven face recognition.
# Features
Dual-Factor Authentication
Access is granted only when:
1. *RFID Card UID matches*, and  
2. *Deep Learning face recognition verifies the user*
   
# AI-Powered Facial Verification
- Uses DeepFace for embeddings  
- Live camera feed capture  
- Automatic distance thresholding  
- Robust even under low lighting

# Real-Time Python - Arduino Communication
- Python reads RFID UID from Arduino  
- Arduino waits for APPROVED / DENIED from Python  
- Motor unlocks only after successful face verification

# Reliable Hardware-Controlled Lock
- Stepper motor rotates lock mechanism  
- Fail-safe design automatically re-locks  
- Clean serial communication handling

# Clean System Workflow
1. User taps RFID card  
2. Arduino sends UID to Python  
3. Python captures face → compares with stored image  
4. If verified → sends **APPROVED**  
5. Arduino unlocks lock for a few seconds  
6. Motor re-locks automatically
   
#Hardware Used
- Arduino UNO / Mega 
- RC522 RFID reader
- RFID card
- A4988 or ULN2003 driver + Stepper Motor (28BYJ-48 or NEMA)  
- USB Webcam (laptop)
- keyboard for input + LCD for display (laptop0
- Jumper wires  
- Breadboard
- LEDs
- Residtors
# How Face Recognition Works (Deep Learning)
- Captures 1 frame from webcam  
- Extracts embeddings using SFace / Facenet  
- Compares embeddings with stored known face  
- If similarity distance < threshold = PASS  
- Otherwise = DENIED  

This method ensures secure and AI-accurate verification compared to older MSE-based methods.

# Stepper Motor into Driver into Arduino
Depends on driver (A4988 or ULN2003).

# Software Installation

1. Install Dependencies  
pip install deepface opencv-python pyserial numpy pillow
2. Run Python Script
python face_reader_deep.py
3. Upload Arduino Code
Use Arduino IDE into upload mahamarduino.ino

# How to Run the System
-Power Arduino
-Run Python script
-Tap RFID card
-Camera opens 
-captures face
-If match 
-Python sends APPROVED
-Motor unlocks
-Auto re-lock

This project is released under the MIT License.
Copyright (c) 2025 Maham Ali
This software is protected under Copyright Law as part of academic intellectual property.
# Author
Maham Ali
Smart AI Access System — 2025
Department of Information Technology

## 📂 Project Structure


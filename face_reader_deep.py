import os
import time
import serial
import cv2
from deepface import DeepFace

# CONFIG

# Arduino serial config
PORT = "COM3"          # Arduino Mega port
BAUD = 9600

# Camera config
CAMERA_INDEX = 0       # 0 for built-in webcam

# Deep learning face reference image
KNOWN_FACE_PATH = r"C:\Users\maiyh\Desktop\known_face\face_1.jpg"

# Allowed RFID card UID text (must match what Arduino prints after CARD_UID:)
ALLOWED_UID_TEXT = "84 5E 39 D9"  

# DeepFace model and threshold
MODEL_NAME = "Facenet512"
DIST_THRESHOLD = 0.60   # smaller = stricter, larger = more lenient



def open_camera(index: int):
    """Open webcam and check it's accessible."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"[PYTHON ERROR] Could not open camera index {index}.")
        raise SystemExit
    return cap


def check_known_face_file():
    """Ensure the reference face image exists before starting."""
    print("[PYTHON] Checking known face reference image...")
    if not os.path.exists(KNOWN_FACE_PATH):
        print(f"[PYTHON ERROR] Reference image not found: {KNOWN_FACE_PATH}")
        raise SystemExit
    print("[PYTHON] Reference image found:", KNOWN_FACE_PATH)


def main():
    check_known_face_file()

    # Open webcam
    cap = open_camera(CAMERA_INDEX)
    print("[PYTHON] Camera opened successfully.")

    # Connect to Arduino
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except Exception as e:
        print(f"[PYTHON ERROR] Could not open serial port {PORT}: {e}")
        cap.release()
        raise SystemExit

    print(f"[PYTHON] Connected to Arduino on {PORT}.")
    print("[PYTHON] Waiting for CARD_UID from Arduino...")

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            print(f"[FROM ARDUINO]: {line}")

            # Expect "CARD_UID: 84 5E 39 D9"
            if line.startswith("CARD_UID"):
                uid_text = line.split(":", 1)[1].strip().upper()

                # 1) Check card UID first
                if uid_text != ALLOWED_UID_TEXT:
                    print("[PYTHON] Wrong card UID. Sending DENIED.")
                    ser.write(b"DENIED\n")
                    # Close any webcam window just in case
                    cv2.destroyAllWindows()
                    continue

                # Show live preview for ~2 seconds
                print("[PYTHON] Correct card. Showing camera preview for 2 seconds for deep learning check...")

                start = time.time()
                last_frame = None

                while time.time() - start < 2.0:
                    ret, frame = cap.read()
                    if not ret:
                        continue

                    # Show the live webcam window
                    cv2.imshow("Deep Learning Face Recognition", frame)
                    last_frame = frame

                    # Allow user to close window with 'q' if needed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                if last_frame is None:
                    print("[PYTHON ERROR] No frame captured from webcam.")
                    ser.write(b"DENIED\n")
                    cv2.destroyAllWindows()
                    continue

                # Run DeepFace verification
                print("[PYTHON AI] Running DeepFace verification...")

                try:
                    # img1 = captured frame (numpy array)
                    # img2 = reference image file on disk
                    result = DeepFace.verify(
                        last_frame,
                        KNOWN_FACE_PATH,
                        model_name=MODEL_NAME,
                        enforce_detection=False
                    )

                    distance = result.get("distance", 1.0)
                    verified = result.get("verified", False)
                    print(f"[PYTHON AI] verified={verified}, distance={distance:.4f}")

                    # Decide using BOTH DeepFace 'verified' flag and our distance threshold
                    if verified and distance < DIST_THRESHOLD:
                        print("[PYTHON AI] FACE MATCH (Deep Learning). Sending APPROVED.")
                        ser.write(b"APPROVED\n")
                    else:
                        print("[PYTHON AI] FACE MISMATCH. Sending DENIED.")
                        ser.write(b"DENIED\n")

                except Exception as e:
                    print(f"[PYTHON AI ERROR] {e}")
                    ser.write(b"DENIED\n")

                # 4) close the webcam window after each check
                cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("\n[PYTHON] CTRL+C detected. Exiting...")

    finally:
        try:
            ser.close()
        except Exception:
            pass

        cap.release()
        cv2.destroyAllWindows()
        print("[PYTHON] Cleaned up. Goodbye.")


if __name__ == "__main__":
    main()

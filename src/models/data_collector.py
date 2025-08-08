import cv2
import csv
import os
import mediapipe as mp

# === Settings ===
LABEL = input("Gesture: ")  # <-- Change this to match the current gesture
CSV_FILE = "data.csv"

# === MediaPipe Hands Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# === Prepare CSV File ===
header = [f"{coord}{i}" for i in range(21) for coord in ("x", "y", "z")] + ["label"]
file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, mode='a', newline='') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(header)  # Add header if new file

    # === Start Webcam ===
    cap = cv2.VideoCapture(0)
    print(f"Ready to collect gesture: '{LABEL}'")
    print("Press 's' to save a sample, 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("❌ Camera read failed.")
            break

        # Flip and convert frame
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display label info
        cv2.putText(frame, f"Label: {LABEL}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Hand Gesture Collector", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("🔚 Quitting.")
            break

        if key == ord('s'):
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                row = []
                for lm in hand.landmark:
                    row.extend([lm.x, lm.y, lm.z])
                row.append(LABEL)
                writer.writerow(row)
                print("✅ Sample saved.")
            else:
                print("⚠️ No hand detected. Try again.")

    cap.release()
    cv2.destroyAllWindows()

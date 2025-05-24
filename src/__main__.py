import cv2
from .camera import HandDetector
from .gesture_recognition import recognize_gesture
from .command_executor import CommandExecutor

def main():
    cap = cv2.VideoCapture(0)  # Open default camera
    # Reduce resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = HandDetector()
    executor = CommandExecutor()

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hands = detector.detect_hands(frame)
        
        if hands:
            # For simplicity, recognize gesture on first hand detected
            gesture = recognize_gesture(hands[0])
            print(f"Gesture detected: {gesture}")
            executor.execute_command(gesture)

        frame = detector.draw_hands(frame, hands)
        detector.draw_hands(frame, hands)        
        cv2.imshow("Hand Gesture Control", frame)
        

        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

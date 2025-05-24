import cv2
from .camera import HandDetector
from .gesture_recognition import GestureDetector
from .command_executor import CommandExecutor

def main():
    cap = cv2.VideoCapture(0)  # Open default camera
    # Reduce resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    hand_detector = HandDetector()
    executor = CommandExecutor()
    gesture_detector = GestureDetector()


    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hands = hand_detector.detect_hands(frame)

        if hands:
            # For simplicity, recognize gesture on first hand detected
            gesture_detector.update(hands[0])
            gesture = gesture_detector.get_gesture()
            print(f"Gesture detected: {gesture}")
            executor.execute_command(gesture)

        frame = hand_detector.draw_hands(frame, hands)
        hand_detector.draw_hands(frame, hands)        
        cv2.imshow("Hand Gesture Control", frame)
        

        if cv2.waitKey(200) & 0xFF == 27:  # Press ESC to quit
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

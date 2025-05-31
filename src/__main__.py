from .hand_detector import HandDetector
from .gesture_recognition import GestureDetector
from .command_executor import CommandExecutor
from .camera import Camera

def main():
    camera = Camera(width=640, height=480)  # Uses OpenCV internally

    hand_detector = HandDetector()
    executor = CommandExecutor()
    gesture_detector = GestureDetector()

    frame_count = 0

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        landmarks = hand_detector.detect_hands(frame)

        if landmarks:
            gesture_detector.update(landmarks)
            gesture = gesture_detector.get_gesture()
            print(f"Gesture detected: {gesture}")
            executor.execute_command(gesture)

        frame = hand_detector.draw_hands(frame)
        camera.show("Hand Gesture Control", frame)

        if camera.wait_key(200) == 27:  # ESC to quit
            break

        frame_count += 1

    camera.release()

if __name__ == "__main__":
    main()

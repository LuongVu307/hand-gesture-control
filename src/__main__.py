from src.hand_detector import HandDetector
from src.gesture_recognition import GestureDetector
from src.command_executor import CommandExecutor
from src.camera import Camera
from src.models.models import HandFeature, HandNormalizer, LandmarkEmbedding



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
            gesture = gesture_detector.get_gesture(landmarks)
            print(f"Gesture detected: {gesture}")
            executor.execute_command(gesture)

        frame = hand_detector.draw_hands(frame)
        camera.show("Hand Gesture Control", frame)

        if camera.wait_key(50) == 27:  # ESC to quit
            break

        frame_count += 1

    camera.release()


if __name__ == "__main__":
    main()

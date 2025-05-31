import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        self.current_multi_hand_landmarks = results.multi_hand_landmarks  # save for drawing
        
        if results.multi_hand_landmarks:
            hands_landmarks = []
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                hand_dict = {
                    "wrist": landmarks[0],
                    "fingers": {
                        "thumb": landmarks[1:5],
                        "index": landmarks[5:9],
                        "middle": landmarks[9:13],
                        "ring": landmarks[13:17],
                        "pinky": landmarks[17:21],
                    }
                }
                hands_landmarks.append(hand_dict)
            return hands_landmarks
        return None

    def draw_hands(self, frame):
        if self.current_multi_hand_landmarks:
            for hand_landmarks in self.current_multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

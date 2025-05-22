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
        """
        Detects hands in the frame.
        Returns: list of hand landmarks if detected, else None
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            hands_landmarks = []
            for hand_landmarks in results.multi_hand_landmarks:
                hands_landmarks.append(hand_landmarks)
            return hands_landmarks
        return None

    def draw_hands(self, frame, hand_landmarks_list):
        """
        Draws hand landmarks on the frame.
        """
        if hand_landmarks_list:
            for hand_landmarks in hand_landmarks_list:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

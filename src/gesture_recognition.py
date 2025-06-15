from src.hand import Hand


class GestureDetector:
    def __init__(self):
        self.hand = Hand()
        self.map = {"open" + "close" * 4: "close", "open" * 5: "open"}

    def update(self, hand_landmarks):
        if hand_landmarks is not None:
            self.hand.update(hand_landmarks[0])

    def map_hand_state(self):
        current_state = self.get_hand_state()
        return self.map[current_state] if current_state in self.map else None

    def get_gesture(self):
        return self.map_hand_state()

    def get_hand_state(self):
        states = []
        for finger_type in ["thumb", "index", "middle", "ring", "pinky"]:
            finger = getattr(self.hand, finger_type)
            states.append(finger.state)

        return "".join(states)

class GestureDetector:
    def __init__(self):
        self.hand = {
            "wrist" : [],
            "thumb" : {},
            "index" : {},
            "middle" : {},
            "ring" : {},
            "pinky" : {},
        }

    def update(self, hand_landmarks):
        self.hand["wrist"] = hand_landmarks[0]
        
        counter = 1
        for finger in self.hand.keys()[1:]:
            self.hand[finger][(counter-1)%4] = hand_landmarks[counter]
            counter += 1

    def get_gesture():
        ...

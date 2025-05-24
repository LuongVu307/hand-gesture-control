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
        if hand_landmarks != None:
            hand_landmarks = hand_landmarks.landmark
            self.hand["wrist"] = hand_landmarks[0]
            
            counter = 1
            for finger in list(self.hand.keys())[1:]:
                self.hand[finger][(counter-1)%4] = hand_landmarks[counter]
                counter += 1

    def get_gesture(self):
        return "open_hand"

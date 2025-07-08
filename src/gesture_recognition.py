import re 

from src.hand import Hand


class GestureDetector:
    def __init__(self):
        self.hand = Hand()
        self.map = {"10000..": "close", 
                    "11111..": "open",
                    "11000.0": "increase",
                    "11000.1": "decrease",
                    }
        
    def update(self, hand_landmarks):
        if hand_landmarks is not None:
            self.hand.update(hand_landmarks[0])

    def map_hand_state(self):
        current_state, flipped, upsidedown = self.get_hand_state()
        # print(flipped, upsidedown)
        flipped, upsidedown = map(lambda x : "1" if x==True else "0", [flipped, upsidedown])
        current_state = current_state + flipped + upsidedown
        # print(current_state)
        hand_state = None
        for item in self.map.keys():
            if re.fullmatch(item, current_state):
                hand_state = self.map[item]
                break       
        # print(hand_state)
        return hand_state

    def get_gesture(self):
        return self.map_hand_state()

    def get_hand_state(self):
        states = []
        for finger_type in ["thumb", "index", "middle", "ring", "pinky"]:
            finger = getattr(self.hand, finger_type)
            states.append(finger.state)

        return "".join(states), self.hand.flipped, self.hand.upsidedown

from .hand import Hand

class GestureDetector:
    def __init__(self):
        self.hand = Hand()
        self.maps = {
            
        }

    def update(self, hand_landmarks):
        if hand_landmarks != None:
            self.hand.update(hand_landmarks[0])

        print(self.hand.get_angle_palm_finger("pinky"))
                    
    def map_hand_state(self):
        return 0
    
    
    def get_gesture(self):
        return self.map_hand_state()
        

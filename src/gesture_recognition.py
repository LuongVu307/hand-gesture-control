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
        self.hand_state = None

    def update(self, hand_landmarks):
        if hand_landmarks != None:
            hand_landmarks = hand_landmarks.landmark
            self.hand["wrist"] = hand_landmarks[0]
            
            multiplier = 0
            for finger in list(self.hand.keys())[1:]:
                for counter in range(4):
                    self.hand[finger][counter] = hand_landmarks[counter+4*multiplier+1]
                multiplier += 1
        
        self.set_hand_state()
        

 
    def get_fingers_state(self):

        finger_states = {
            "thumb" : None,
            "index" : None,
            "middle" : None,
            "ring" : None,
            "pinky" : None,
        }


        for finger in list(self.hand.keys())[1:]:
            if self.hand[finger][3].y < self.hand[finger][2].y < self.hand[finger][1].y < self.hand[finger][0].y:
                finger_states[finger] = "fully_open"
            elif self.hand[finger][1].y < self.hand[finger][3].y < self.hand[finger][2].y:
                finger_states[finger] = "fully_closed"
            elif self.hand[finger][1].y < self.hand[finger][2].y < self.hand[finger][3].y:
                finger_states[finger] = "half_closed"
        return finger_states
            
    
    def set_hand_state(self):
        finger_states = self.get_fingers_state()
        print(finger_states.values())
        
        if (len(set(finger_states.values()))==1) and ("fully_open" in finger_states.values()):
            self.hand_state = "fully_open_hand"
        else:
            self.hand_state = "close_hand"
            for finger in ["index", "middle", "ring", "pinky"]:
                if finger_states[finger] not in ["fully_closed", "half_closed"]:
                    self.hand_state = None
                    break

            

    def get_gesture(self):
        return self.hand_state
        

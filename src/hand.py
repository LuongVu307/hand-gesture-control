import math

# Assuming the hand detected is right hand
class Hand:
    def __init__(self):
        self.thumb, self.index, self.middle, self.ring, self.pinky = \
            Finger("thumb"), Finger("index"), Finger("middle"), Finger("ring"), Finger("pinky")
        self.wrist = None

    @property
    def fingers(self):
        return {
            self.thumb.type : self.thumb,
            self.index.type: self.index,
            self.middle.type: self.middle,
            self.ring.type: self.ring,
            self.pinky.type: self.pinky, 
        }
    
    @fingers.setter
    def fingers(self, finger_landmarks):
        for finger_type, landmarks in finger_landmarks.items():
            if finger_type in self.fingers:
                # Assuming each Finger object has an update_landmarks method or similar
                self.fingers[finger_type].update(landmarks)



class Finger:
    def __init__(self, type):
        self.type = type
        self.base, self.first, self.second, self.tip = None, None, None, None

    def update(self, landmarks):
        self.base = landmarks[0]
        self.first = landmarks[1]
        self.second = landmarks[2]
        self.tip = landmarks[3]


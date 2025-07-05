# Assuming the hand detected is right hand
class Hand:
    def __init__(self):
        self.thumb, self.index, self.middle, self.ring, self.pinky = (
            Finger("thumb"),
            Finger("index"),
            Finger("middle"),
            Finger("ring"),
            Finger("pinky"),
        )
        self.wrist = None
        self.flipped, self.upsidedown = False, False

    @property
    def fingers(self):
        return {
            self.thumb.type: self.thumb,
            self.index.type: self.index,
            self.middle.type: self.middle,
            self.ring.type: self.ring,
            self.pinky.type: self.pinky,
        }

    @fingers.setter
    def fingers(self, finger_landmarks):
        for finger_type, landmarks in finger_landmarks.items():
            if finger_type in self.fingers:
                # Assuming each Finger object has an update_landmarks
                # method or similar
                self.fingers[finger_type].update(landmarks)

    def update(self, landmarks):
        self.wrist = landmarks["wrist"]
        self.fingers = landmarks["fingers"]
        self.normalize()

    # Assume the fingers position never cross each other.
    # Ex: fingers are always in the position thumb->index->middle->ring->pinky
    # or reversed
    def normalize(self):
        # Flip horizontally if thumb is to the left of pinky
        # The palm is not facing the camera)
        thumb_less_pinky = self.thumb.x < self.pinky.x 
        wrist_less_middle = self.wrist.y < self.middle.tip.y

        if thumb_less_pinky and wrist_less_middle:
            self.flipped = False
            self.upsidedown = True

            for finger in self.fingers.values():
                finger.flip_horizontal(self.wrist.x)

            for finger in self.fingers.values():
                finger.flip_vertical(self.wrist.y)


        elif not thumb_less_pinky and not wrist_less_middle:
            self.flipped = False
            self.upsidedown = False
        elif not thumb_less_pinky and wrist_less_middle:
            self.flipped = True
            self.upsidedown = True

            for finger in self.fingers.values():
                finger.flip_vertical(self.wrist.y)

        elif thumb_less_pinky and not wrist_less_middle:
            self.flipped = True
            self.upsidedown = False

            for finger in self.fingers.values():
                finger.flip_horizontal(self.wrist.x)




class Finger:
    VALID_TYPES = ["thumb", "index", "middle", "ring", "pinky"]
    JOIN_NAMES = ["base", "first", "second", "tip"]

    def __init__(self, type="null"):
        if type not in self.VALID_TYPES:
            raise ValueError("Invalid finger type")
        self.type = type
        self.base, self.first, self.second, self.tip = None, None, None, None

    def update(self, landmarks):
        self.base, self.first, self.second, self.tip = landmarks

    def flip_horizontal(self, wrist_x):
        for joint_name in self.JOIN_NAMES:
            joint = getattr(self, joint_name)
            if joint is not None:
                joint.x = 2 * wrist_x - joint.x

    def flip_vertical(self, wrist_y):
        for joint_name in self.JOIN_NAMES:
            joint = getattr(self, joint_name)
            if joint is not None:
                joint.y = 2 * wrist_y - joint.y

    @property
    def x(self):
        return sum(j.x for j in self.joints if j) / 4

    @property
    def y(self):
        return sum(j.y for j in self.joints if j) / 4

    @property
    def z(self):
        return sum(j.z for j in self.joints if j) / 4

    @property
    def joints(self):
        return [self.base, self.first, self.second, self.tip]

    @property
    def state(self):
        if self.tip.y < self.base.y:
            return "1"
        else:
            return "0"

import pytest

from src.hand import Hand

@pytest.fixture
def sample_landmark(mocker):
    coord = (0.42, 0.12, 0.76)
    landmark_mock = mocker.Mock()
    landmark_mock.x = coord[0]
    landmark_mock.y = coord[1]
    landmark_mock.z = coord[2]

    return coord, landmark_mock

@pytest.fixture
def landmark_without_wrist(mocker):
    landmarks = {}

    for finger in ["thumb", "index", "middle", "ring", "pinky"]:
        temp = []
        for _ in ["base", "first", "second", "tip"]:
            landmark_mock = mocker.Mock()
            landmark_mock.x = 0.42
            landmark_mock.y = 0.12
            landmark_mock.z = 0.76
            temp.append(landmark_mock)

        landmarks[finger] = temp

    return landmarks

@pytest.fixture
def landmark_with_wrist(sample_landmark, landmark_without_wrist):
    hand_landmark = {}

    finger_landmarks = landmark_without_wrist
    coord, wrist_landmark = sample_landmark

    hand_landmark["wrist"] = wrist_landmark
    hand_landmark["fingers"] = finger_landmarks

    return hand_landmark

@pytest.mark.parametrize("finger_name", [
    "thumb", "index", "middle", "ring", "pinky"
])
def test_hand_init_finger_valid(finger_name, mocker):
    mock_finger = mocker.Mock()
    mock_finger.type = finger_name

    hand = Hand()

    assert hand.fingers[finger_name].type == finger_name
    assert hand.fingers[finger_name].base == None
    assert hand.fingers[finger_name].first == None
    assert hand.fingers[finger_name].second == None
    assert hand.fingers[finger_name].tip == None

def test_hand_init_wrist_valid():
    
    hand = Hand()
    assert hand.wrist == None

def test_hand_finger_setter_valid(landmark_without_wrist, sample_landmark):
    landmarks = landmark_without_wrist
    coord, _ = sample_landmark

    hand = Hand()

    hand.fingers = landmarks
    for finger in ["thumb", "index", "middle", "ring", "pinky"]:
        assert hand.fingers[finger].base.x == coord[0]
        assert hand.fingers[finger].base.y == coord[1]
        assert hand.fingers[finger].base.z == coord[2]

        assert hand.fingers[finger].first.x == coord[0]
        assert hand.fingers[finger].first.y == coord[1]
        assert hand.fingers[finger].first.z == coord[2]

        assert hand.fingers[finger].second.x == coord[0]
        assert hand.fingers[finger].second.y == coord[1]
        assert hand.fingers[finger].second.z == coord[2]

        assert hand.fingers[finger].tip.x == coord[0]
        assert hand.fingers[finger].tip.y == coord[1]
        assert hand.fingers[finger].tip.z == coord[2]

def test_hand_update(landmark_with_wrist, sample_landmark):
    hand_landmark = landmark_with_wrist    
    coord, _ = sample_landmark

    hand = Hand()
    hand.update(hand_landmark)

    for finger in ["thumb", "index", "middle", "ring", "pinky"]:
        assert hand.fingers[finger].base.x == coord[0]
        assert hand.fingers[finger].base.y == coord[1]
        assert hand.fingers[finger].base.z == coord[2]

        assert hand.fingers[finger].first.x == coord[0]
        assert hand.fingers[finger].first.y == coord[1]
        assert hand.fingers[finger].first.z == coord[2]

        assert hand.fingers[finger].second.x == coord[0]
        assert hand.fingers[finger].second.y == coord[1]
        assert hand.fingers[finger].second.z == coord[2]

        assert hand.fingers[finger].tip.x == coord[0]
        assert hand.fingers[finger].tip.y == coord[1]
        assert hand.fingers[finger].tip.z == coord[2]

        assert hand.wrist.x == coord[0]
        assert hand.wrist.y == coord[1]
        assert hand.wrist.z == coord[2]

@pytest.mark.parametrize("wrist_y, middle_tip_y, thumb_x, pinky_x, upsidedown, flipped", [
    (0.1, 0.2, 0.3, 0.4, True, True),
    (0.2, 0.1, 0.4, 0.3, False, False)
])
def test_hand_normalize(wrist_y, middle_tip_y, thumb_x, pinky_x, upsidedown, flipped, landmark_with_wrist, sample_landmark):
    hand_landmark = landmark_with_wrist    
    coord, _ = sample_landmark

    hand = Hand()
    hand.update(hand_landmark)

    hand.wrist.y = float(wrist_y)

    hand.middle.tip.y = middle_tip_y

    hand.thumb.base.x = thumb_x
    hand.thumb.first.x = thumb_x
    hand.thumb.second.x = thumb_x
    hand.thumb.tip.x = thumb_x

    hand.pinky.base.x = pinky_x
    hand.pinky.first.x = pinky_x
    hand.pinky.second.x = pinky_x
    hand.pinky.tip.x = pinky_x


    hand.normalize()

    assert hand.upsidedown == upsidedown
    assert hand.flipped == flipped


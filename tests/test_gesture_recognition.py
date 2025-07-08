import pytest
from src.gesture_recognition import GestureDetector

@pytest.fixture
def fake_hand_landmarks(mocker):
    return [{
        'wrist': mocker.MagicMock(x=0.213, y=0.679, z=5.1e-7),
        'fingers': {
            'thumb': [
                mocker.MagicMock(x=0.270, y=0.686, z=-0.025),
                mocker.MagicMock(x=0.331, y=0.633, z=-0.031),
                mocker.MagicMock(x=0.376, y=0.585, z=-0.033),
                mocker.MagicMock(x=0.413, y=0.557, z=-0.035),
            ],
            'index': [
                mocker.MagicMock(x=0.316, y=0.530, z=-0.021),
                mocker.MagicMock(x=0.360, y=0.466, z=-0.034),
                mocker.MagicMock(x=0.391, y=0.429, z=-0.043),
                mocker.MagicMock(x=0.415, y=0.398, z=-0.051),
            ],
            'middle': [
                mocker.MagicMock(x=0.286, y=0.499, z=-0.019),
                mocker.MagicMock(x=0.325, y=0.422, z=-0.032),
                mocker.MagicMock(x=0.357, y=0.377, z=-0.043),
                mocker.MagicMock(x=0.384, y=0.341, z=-0.052),
            ],
            'ring': [
                mocker.MagicMock(x=0.251, y=0.486, z=-0.020),
                mocker.MagicMock(x=0.273, y=0.400, z=-0.036),
                mocker.MagicMock(x=0.296, y=0.349, z=-0.051),
                mocker.MagicMock(x=0.318, y=0.308, z=-0.061),
            ],
            'pinky': [
                mocker.MagicMock(x=0.216, y=0.490, z=-0.023),
                mocker.MagicMock(x=0.228, y=0.422, z=-0.040),
                mocker.MagicMock(x=0.241, y=0.377, z=-0.052),
                mocker.MagicMock(x=0.256, y=0.336, z=-0.060),
            ],
        }
    }]


@pytest.fixture
def mock_hand_class(mocker):
    # Patch src.hand.Hand
    mock_hand_cls = mocker.patch("src.gesture_recognition.Hand")
    return mock_hand_cls


def test_update_calls_hand_update(mock_hand_class, fake_hand_landmarks):
    detector = GestureDetector()

    mock_hand_class.assert_called_once()

    mock_hand_instance = mock_hand_class.return_value

    detector.update(fake_hand_landmarks)

    mock_hand_instance.update.assert_called_once_with(fake_hand_landmarks[0])


def test_map_hand_state_open(mocker, mock_hand_class):
    detector = GestureDetector()

    # Set all finger states to "open"
    for finger in ["thumb", "index", "middle", "ring", "pinky"]:
        setattr(getattr(mock_hand_class.return_value, finger), "state", "1")

    gesture = detector.get_gesture()
    assert gesture == "open"


def test_map_hand_state_close(mocker, mock_hand_class):
    detector = GestureDetector()

    # Set thumb open and others close
    setattr(getattr(mock_hand_class.return_value, "thumb"), "state", "1")
    for finger in ["index", "middle", "ring", "pinky"]:
        setattr(getattr(mock_hand_class.return_value, finger), "state", "0")


    gesture = detector.get_gesture()
    assert gesture == "close"



def test_get_gesture_calls_map_hand_state(mocker, mock_hand_class):
    detector = GestureDetector()
    mocked_map_hand_state = mocker.patch.object(detector, "map_hand_state", return_value="mocked_gesture")

    result = detector.get_gesture()

    assert result == "mocked_gesture"
    mocked_map_hand_state.assert_called_once()

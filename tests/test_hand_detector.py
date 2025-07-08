import pytest
import numpy as np
from src.hand_detector import HandDetector


@pytest.fixture
def fake_frame():
    # Create a fake OpenCV image (480x640 RGB)
    return np.zeros((480, 640, 3), dtype=np.uint8)


def test_detect_hands_with_landmarks(mocker, fake_frame):
    # Arrange: Patch MediaPipe Hands API
    mock_hands_instance = mocker.MagicMock()
    mock_hands_process = mock_hands_instance.process

    fake_landmark = mocker.MagicMock()
    fake_landmark.landmark = [mocker.MagicMock() for _ in range(21)]
    mock_results = mocker.MagicMock(multi_hand_landmarks=[fake_landmark])
    mock_hands_process.return_value = mock_results

    mock_hands_class = mocker.patch("src.hand_detector.mp.solutions.hands.Hands", return_value=mock_hands_instance)
    mocker.patch("cv2.cvtColor", return_value="fake_rgb_image")

    detector = HandDetector()

    # Act
    result = detector.detect_hands(fake_frame)

    # Assert
    mock_hands_class.assert_called_once()
    mock_hands_instance.process.assert_called_once_with("fake_rgb_image")
    assert result is not None
    assert isinstance(result, list)
    assert "wrist" in result[0]
    assert "fingers" in result[0]
    assert len(result[0]["fingers"]["thumb"]) == 4

    # Check internal state
    assert detector.current_multi_hand_landmarks == mock_results.multi_hand_landmarks


def test_detect_hands_without_landmarks(mocker, fake_frame):
    # Arrange
    mocker.patch("cv2.cvtColor", return_value="fake_rgb_image")
    detector = HandDetector()
    detector.hands.process = mocker.MagicMock(return_value=mocker.MagicMock(multi_hand_landmarks=None))

    # Act
    result = detector.detect_hands(fake_frame)

    # Assert
    assert result is None
    assert detector.current_multi_hand_landmarks is None


def test_draw_hands_calls_draw_landmarks(mocker, fake_frame):
    # Arrange
    detector = HandDetector()
    mock_draw_landmarks = mocker.patch.object(detector.mp_draw, "draw_landmarks")
    fake_landmark = mocker.MagicMock()
    detector.current_multi_hand_landmarks = [fake_landmark]

    # Act
    returned_frame = detector.draw_hands(fake_frame)

    # Assert
    mock_draw_landmarks.assert_called_once_with(
        fake_frame, fake_landmark, detector.mp_hands.HAND_CONNECTIONS
    )
    assert returned_frame is fake_frame

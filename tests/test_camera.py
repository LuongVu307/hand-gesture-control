import cv2
import pytest
from src.camera import Camera  # Replace `your_module` with your file name (no .py)

def test_camera_init_and_release(mocker):
    # Mock cv2.VideoCapture
    mock_cap = mocker.MagicMock()
    mock_cap.isOpened.return_value = True

    # Patch cv2.VideoCapture to return mock_cap
    mocker.patch("cv2.VideoCapture", return_value=mock_cap)

    # Patch cv2.destroyAllWindows
    mock_destroy = mocker.patch("cv2.destroyAllWindows")

    cam = Camera(width=800, height=600, cam_index=1)

    # Assert VideoCapture was called
    cv2.VideoCapture.assert_called_with(1)

    # Assert width and height were set
    mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_WIDTH, 800)
    mock_cap.set.assert_any_call(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    # Release camera
    cam.release()
    mock_cap.release.assert_called_once()
    mock_destroy.assert_called_once()

def test_get_frame_returns_frame(mocker):
    mock_cap = mocker.MagicMock()
    mock_cap.read.return_value = (True, "fake_frame")

    mocker.patch("cv2.VideoCapture", return_value=mock_cap)

    cam = Camera()
    frame = cam.get_frame()
    assert frame == "fake_frame"

def test_get_frame_returns_none_on_failure(mocker):
    mock_cap = mocker.MagicMock()
    mock_cap.read.return_value = (False, None)

    mocker.patch("cv2.VideoCapture", return_value=mock_cap)

    cam = Camera()
    frame = cam.get_frame()
    assert frame is None

def test_show_calls_imshow(mocker):
    # Patch cv2.imshow
    mock_imshow = mocker.patch("cv2.imshow")

    cam = Camera()
    cam.show("TestWindow", "FakeFrame")

    # Assert cv2.imshow was called with correct arguments
    mock_imshow.assert_called_once_with("TestWindow", "FakeFrame")

def test_wait_key_returns_key_code(mocker):
    # Patch cv2.waitKey to return a fake key code
    mock_waitKey = mocker.patch("cv2.waitKey", return_value=0x41)  # Example: ASCII for 'A'

    cam = Camera()
    key = cam.wait_key(10)

    # Check waitKey was called with delay=10
    mock_waitKey.assert_called_once_with(10)

    # Check returned key code (should AND with 0xFF)
    assert key == 0x41 & 0xFF  # Should equal 0x41

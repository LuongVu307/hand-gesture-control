import pytest

from src.hand import Finger


@pytest.fixture
def finger():
    return Finger("ring")


@pytest.fixture
def mock_joint(mocker):
    def _make_joint(x, y, z):
        joint = mocker.Mock()
        joint.x = x
        joint.y = y
        joint.z = z
        return joint

    return _make_joint


@pytest.mark.parametrize(
    "finger_type", [("thumb"), ("index"), ("middle"), ("ring"), ("pinky")]
)
def test_finger_init_valid(finger_type):
    finger = Finger(finger_type)
    assert finger.type == finger_type


@pytest.mark.parametrize(
    "finger_type, error_msg",
    [
        ("null", "Invalid finger type"),
        ("", "Invalid finger type"),
        (None, "Invalid finger type"),
    ],
)
def test_finger_init_invalid(finger_type, error_msg):
    with pytest.raises(ValueError, match=error_msg):
        Finger(finger_type)


def test_finger_init_missing_arg():
    with pytest.raises(ValueError, match="Invalid finger type"):
        Finger()


def test_finger_update(finger, mocker):

    lms = []
    coords = [
        (0.1, 0.2, 0.3),
        (0.1, 0.2, 0.3),
        (0.1, 0.2, 0.3),
        (0.1, 0.2, 0.3),
    ]

    for x, y, z in coords:
        lm = mocker.Mock()
        lm = mocker.Mock(x=x, y=y, z=z)

        lms.append(lm)

    finger.update(lms)

    assert finger.base.x == 0.1
    assert finger.base.y == 0.2
    assert finger.base.z == 0.3

    assert finger.first.x == 0.1
    assert finger.first.y == 0.2
    assert finger.first.z == 0.3

    assert finger.second.x == 0.1
    assert finger.second.y == 0.2
    assert finger.second.z == 0.3

    assert finger.tip.x == 0.1
    assert finger.tip.y == 0.2
    assert finger.tip.z == 0.3

    assert finger.x == (0.1 + 0.1 + 0.1 + 0.1) / 4
    assert finger.y == (0.2 + 0.2 + 0.2 + 0.2) / 4
    assert finger.z == (0.3 + 0.3 + 0.3 + 0.3) / 4

    assert finger.joints == lms


@pytest.mark.parametrize(
    "tip_y, base_y, exp_val",
    [
        (0.2, 0.4, "open"),
        (0.0, 0.0, "close"),
        (0.9, 0.3, "close"),
    ],
)
def test_finger_state(tip_y, base_y, exp_val, mocker):
    finger = Finger("index")
    finger.tip = mocker.Mock()
    finger.tip.y = tip_y

    finger.base = mocker.Mock()
    finger.base.y = base_y

    assert finger.state == exp_val

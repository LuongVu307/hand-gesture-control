import pytest
import numpy as np

@pytest.fixture
def blank_frame():
    return np.zeros((480, 640, 3), dtype=np.uint8)

@pytest.fixture
def dummy_hand_box():
    return (100, 100, 200, 200)

import pytest
from src.utils import is_audio_playing


def test_is_audio_playing_returns_true(mocker):
    # Arrange: Create a mock session with State = 1 (active) and a Process
    mock_session = mocker.MagicMock()
    mock_session.State = 1
    mock_session.Process = True

    # Patch AudioUtilities.GetAllSessions to return a list with the active session
    mock_get_sessions = mocker.patch(
        "src.utils.AudioUtilities.GetAllSessions",
        return_value=[mock_session]
    )

    # Act
    result = is_audio_playing()

    # Assert
    assert result is True
    mock_get_sessions.assert_called_once()


def test_is_audio_playing_returns_false_when_no_active_sessions(mocker):
    # Arrange: Create a mock session with State != 1 (inactive)
    mock_session = mocker.MagicMock()
    mock_session.State = 0  # inactive
    mock_session.Process = True

    # Patch AudioUtilities.GetAllSessions to return a list with inactive sessions
    mock_get_sessions = mocker.patch(
        "src.utils.AudioUtilities.GetAllSessions",
        return_value=[mock_session]
    )

    # Act
    result = is_audio_playing()

    # Assert
    assert result is False
    mock_get_sessions.assert_called_once()


def test_is_audio_playing_returns_false_when_no_sessions(mocker):
    # Arrange: Patch GetAllSessions to return an empty list
    mock_get_sessions = mocker.patch(
        "src.utils.AudioUtilities.GetAllSessions",
        return_value=[]
    )

    # Act
    result = is_audio_playing()

    # Assert
    assert result is False
    mock_get_sessions.assert_called_once()

import pytest
from src.command_executor import CommandExecutor  # adjust import if needed

def test_execute_command_close_when_not_playing(mocker):
    # Mock is_audio_playing to return False
    mocker.patch("src.utils.is_audio_playing", return_value=False)

    # Mock pyautogui.press
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    assert executor.playing is False  # Initially not playing

    executor.execute_command("close")

    # Should press playpause and update state
    mock_press.assert_called_once_with("playpause")
    assert executor.playing is True

def test_execute_command_close_when_already_playing(mocker):
    mocker.patch("src.command_executor.is_audio_playing", return_value=True)
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    assert executor.playing is True  # Initially playing

    executor.execute_command("close")

    # Should not press playpause because already playing
    mock_press.assert_not_called()
    assert executor.playing is True

def test_execute_command_open_when_playing(mocker):
    mocker.patch("src.command_executor.is_audio_playing", return_value=True)
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    assert executor.playing is True

    executor.execute_command("open")

    # Should press playpause and update state
    mock_press.assert_called_once_with("playpause")
    assert executor.playing is False

def test_execute_command_open_when_not_playing(mocker):
    mocker.patch("src.utils.is_audio_playing", return_value=False)
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    assert executor.playing is False

    executor.execute_command("open")

    # Should not press playpause because already not playing
    mock_press.assert_not_called()
    assert executor.playing is False

def test_execute_command_unknown(mocker, capsys):
    mocker.patch("src.utils.is_audio_playing", return_value=True)
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.execute_command("foobar")

    # Should print unknown command
    captured = capsys.readouterr()
    assert "Unknown command: foobar" in captured.out

    # Should not press any key
    mock_press.assert_not_called()

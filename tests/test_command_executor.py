import pytest
from src.command_executor import CommandExecutor  # adjust import if needed

import pytest
from src.command_executor import CommandExecutor

def test_execute_command_close_when_not_playing(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.playing = False

    executor.execute_command("close")

    mock_press.assert_called_once_with("playpause")
    assert executor.playing is True

def test_execute_command_close_when_already_playing(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.playing = True

    executor.execute_command("close")

    mock_press.assert_not_called()
    assert executor.playing is True

def test_execute_command_open_when_playing(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.playing = True

    executor.execute_command("open")

    mock_press.assert_called_once_with("playpause")
    assert executor.playing is False

def test_execute_command_increase_volume(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()

    executor.execute_command("increase")

    mock_press.assert_called_once_with("volumeup")

def test_execute_command_decrease_volume(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()

    executor.execute_command("decrease")

    mock_press.assert_called_once_with("volumedown")

def test_execute_command_open_when_not_playing(mocker):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.playing = False

    executor.execute_command("open")

    mock_press.assert_not_called()
    assert executor.playing is False

def test_execute_command_unknown(mocker, capsys):
    mock_press = mocker.patch("pyautogui.press")

    executor = CommandExecutor()
    executor.execute_command("foobar")

    captured = capsys.readouterr()
    assert "Unknown command: foobar" in captured.out

    mock_press.assert_not_called()

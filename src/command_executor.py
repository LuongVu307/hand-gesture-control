import pyautogui
from .utils import is_audio_playing


class CommandExecutor:
    def __init__(self):
        self.playing = is_audio_playing()

    def execute_command(self, command_name):
        """
        Map recognized gesture names to actions.
        Extend this as you add more gestures.
        """

        if command_name == "close":
            if self.playing is False:
                pyautogui.press("playpause")
                self.playing = True
        elif command_name == "open":
            if self.playing is True:
                pyautogui.press("playpause")
                self.playing = False
        else:
            print(f"Unknown command: {command_name}")

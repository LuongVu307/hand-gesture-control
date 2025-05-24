import pyautogui
from .utils import is_audio_playing

class CommandExecutor:
    def __init__(self):
        self.play_state = is_audio_playing()

    def execute_command(self, command_name):
        """
        Map recognized gesture names to actions.
        Extend this as you add more gestures.
        """
        
        if command_name == "close_hand":
            if self.play_state ==False:
                pyautogui.press('playpause')
                self.play_state = True
        elif command_name == "fully_open_hand":
            if self.play_state == True:
                pyautogui.press('playpause')
                self.play_state = False
        else:
            print(f"Unknown command: {command_name}")

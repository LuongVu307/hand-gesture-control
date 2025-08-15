import pyautogui


class CommandExecutor:
    def __init__(self):
        self.playing = False

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
        elif command_name == "point_up":
            pyautogui.press("volumeup")
        elif command_name == "point_down":
            pyautogui.press("volumedown")
        else:
            print(f"Unknown command: {command_name}")

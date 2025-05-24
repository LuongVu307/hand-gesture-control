import pyautogui

class CommandExecutor:
    def __init__(self):
        self.play_state = None

    def execute_command(self, command_name):
        """
        Map recognized gesture names to actions.
        Extend this as you add more gestures.
        """
        if command_name == "fist":
            pyautogui.press('pause')
            self.play_state = False
        elif command_name == "open_hand" and self.play_state == False:
            pyautogui.press('play')
            self.play_state = True

        else:
            print(f"Unknown command: {command_name}")

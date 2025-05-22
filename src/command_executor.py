import pyautogui

class CommandExecutor:
    def __init__(self):
        pass

    def execute_command(self, command_name):
        """
        Map recognized gesture names to actions.
        Extend this as you add more gestures.
        """
        if command_name == "fist":
            pyautogui.press('space')  # Example: Press space bar
        elif command_name == "open_hand":
            pyautogui.press('enter')  # Example: Press enter
        # Add more mappings here
        else:
            print(f"Unknown command: {command_name}")

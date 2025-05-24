# utils.py
from pycaw.pycaw import AudioUtilities

def is_audio_playing():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        # session.State == 1 means the session is active (playing audio)
        if session.Process and session.State == 1:
            return True
    return False

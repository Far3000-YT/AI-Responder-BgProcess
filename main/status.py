import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#use dotfile for hidden status
STATUS_FILE = os.path.join(BASE_DIR, ".ai_status")

def set_status(status_text):
    """writes the current status to the status file"""
    try:
        with open(STATUS_FILE, "w") as f:
            f.write(status_text)
    except IOError as e:
        print(f"Error writing status file {STATUS_FILE}: {e}")

def clear_status():
    """removes the status file"""
    try:
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)
    except IOError as e:
        print(f"Error clearing status file {STATUS_FILE}: {e}")

def is_busy():
    """checks if the status file exists, indicating a request is in progress"""
    return os.path.exists(STATUS_FILE)

#initial cleanup on script start
clear_status()
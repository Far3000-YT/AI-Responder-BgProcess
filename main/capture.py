import pyautogui
import time
import keyboard
import os

from .c_config import config as app_config
ps_key = app_config.get("point_select", "ctrl")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_SCREENSHOT_PATH = os.path.join(BASE_DIR, "temp_screenshot.png")

def take_screenshot():
    """waits for two 'point_select' key presses, takes screenshot, saves temp file"""
    print(f"Press '{ps_key}' to select the first point...")
    m1 = None
    m2 = None

    try:
        #wait for first point
        while True:
            #check for esc cancel
            if keyboard.is_pressed('esc'):
                 print("Screenshot capture cancelled.")
                 return None
            if keyboard.is_pressed(ps_key):
                m1 = pyautogui.position()
                print("Point 1 captured.")
                #debounce key press
                time.sleep(0.5)
                break
            #prevent high cpu usage
            time.sleep(0.01)

        #wait for second point
        print(f"Press '{ps_key}' to select the second point...")
        while True:
             #check for esc cancel
             if keyboard.is_pressed('esc'):
                 print("Screenshot capture cancelled.")
                 return None
             if keyboard.is_pressed(ps_key):
                m2 = pyautogui.position()
                print("Point 2 captured.")
                #debounce key press
                time.sleep(0.5)
                break
             #prevent high cpu usage
             time.sleep(0.01)

        if m1 and m2:
            x1, y1 = m1
            x2, y2 = m2
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            print(f"Screenshot region: ({left}, {top}, {width}, {height})")

            #check for zero size region
            if width <= 0 or height <= 0:
                print("Error: Screenshot region has zero width or height. Cannot capture.")
                return None

            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(TEMP_SCREENSHOT_PATH)
            print(f"Screenshot saved to {TEMP_SCREENSHOT_PATH}")
            return TEMP_SCREENSHOT_PATH

    except Exception as e:
        print(f"Error during screenshot process: {e}")
        return None

def cleanup_screenshot(image_path):
    """deletes the temporary screenshot file if it exists"""
    #ensure deleting the correct temp file, not arbitrary path
    expected_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp_screenshot.png")
    if image_path and image_path == expected_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"Cleaned up screenshot file: {image_path}")
        except Exception as e:
            print(f"Error cleaning up screenshot file {image_path}: {e}")
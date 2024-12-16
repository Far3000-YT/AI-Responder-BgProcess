import pyautogui, time, pyperclip, keyboard, threading, os, yaml, comtypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import Image
import google.generativeai as genai

#define variables from yaml file
with open("config.yaml", "r+", encoding="utf-8") as file:
    data = yaml.safe_load(file)

mn = data["model_name"]
bp = data["base_prompt"]
sr = data["short_response"]
dr = data["double_requests"]
sc = data["screenshot_cmd"]
ps = data["point_select"]
cc = data["ctrl_c"]
pf = data["promptf"]
mat = data["max_output_tokens"]
tk = data["top_k"]

#Def sys sounds (0, 1, mute)
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

def mute_sound():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)

def unmute_sound():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(0, None)

loading = False

def blink():
    global loading
    set_volume(0)
    while loading:
        mute_sound()
        time.sleep(1.5)
        unmute_sound()
        time.sleep(1.5)

genai.configure(api_key = os.environ['API_KEY_GEMINI'])

config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": tk,
    "max_output_tokens": mat,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name = mn, generation_config = config)

def prompt_f(output_text):
    text2 = f"""
    {pf}

    {output_text}
    """
    return text2

def take_screenshot():
    try:
        m1 = None
        m2 = None

        while True:
            if keyboard.is_pressed(ps):
                m1 = pyautogui.position()
                print("p1 taken")
                time.sleep(0.5)
                break

        while True:
            if keyboard.is_pressed(ps):
                m2 = pyautogui.position()
                print("p2 taken")
                time.sleep(0.5)
                break
        
        if m1 and m2:
            x1, y1 = m1
            x2, y2 = m2
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            print(x1, y1, x2, y2)
            screenshot = pyautogui.screenshot(region = (left, top, width, height))
            screenshot_path = "temp_screenshot.png"
            screenshot.save(screenshot_path)
            return screenshot_path
        
    except Exception as e:
        print(f"error : {e}")

def send_to_gemini_dr(i, image_path, prompt):
    global loading

    try:
        if i == 0:
            genai.configure(api_key = os.environ['API_KEY_GEMINI'])

            config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": tk,
            "max_output_tokens": mat,
            "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(model_name = mn, generation_config = config)
            print("changed api key to first")

        elif i == 1:
            genai.configure(api_key = os.environ['API_KEY_GEMINI2'])

            config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": tk,
            "max_output_tokens": mat,
            "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(model_name = mn, generation_config = config)
            print("changed api key to second")

        loading = True
        thread = threading.Thread(target = blink)
        thread.start()

        if image_path == "": 
            response = model.generate_content([prompt])
        
        else:
            with open(image_path, "rb") as image_file:
                image_file = Image.open(image_file)
                response = model.generate_content([prompt, image_file])

        loading = False
        thread.join() 

        return response.text
        
    except Exception as e:
        print(f"error : {e}")

        loading = False
        thread.join() 

        return "req error"

def send_to_gemini(image_path, prompt):
    global loading

    loading = True
    thread = threading.Thread(target = blink)
    thread.start()

    try:
        if image_path == "":
            response = model.generate_content([prompt])
        
        else:
            with open(image_path, "rb") as image_file:
                image_file = Image.open(image_file)
                response = model.generate_content([prompt, image_file])

        loading = False
        thread.join()

        return response.text
        
    except Exception as e:
        print(f"error : {e}")

        loading = False
        thread.join() 

        return "req error"
  
def listen_for_commands():
    print("Script running in background")

    last_execution_time = 0
    cooldown = 30

    while True:
        current_time = time.time()

        if keyboard.is_pressed(sc):
            if current_time - last_execution_time >= cooldown:
                last_execution_time = current_time

                print("Screenshot command detected, take 2 points to screenshot...")

                time.sleep(0.5)
                image_path = take_screenshot()

                if dr: input = send_to_gemini_dr(0, image_path, bp)
                else: input = send_to_gemini(image_path, bp)

                if input: print("First input done")
                time.sleep(1)

                if sr:
                    if dr: input = send_to_gemini_dr(1, "", prompt_f(input))
                    else: input = send_to_gemini("", prompt_f(input))
                    if input: print("Output copied to clipboard \n")
                pyperclip.copy(input)
                time.sleep(1)

            else:
                pyperclip.copy("w8")
                print("pls wait till 30 sec for request")

        if keyboard.is_pressed('ctrl+c'):
            if cc:
                if current_time - last_execution_time >= cooldown:
                    last_execution_time = current_time
                    print("Ctrlc command detected")
                    time.sleep(0.05)
                    text_input = pyperclip.paste()

                    if dr: input = send_to_gemini_dr(0, "", f"{text_input} \n {bp}")
                    else: input = send_to_gemini("", f"{text_input} \n {bp}")
                    if input: print("First input done")
                    time.sleep(1)

                    if sr:
                        if dr: input = send_to_gemini_dr(1, "", prompt_f(input))
                        else: input = send_to_gemini("", prompt_f(input))
                        if input: print("Output copied to clipboard \n")
                    pyperclip.copy(input)
                    time.sleep(1)

                else:
                    pyperclip.copy("w8")
                    print("pls wait till 30 sec for request")
        
        if keyboard.is_pressed('ctrl+v'):
            print("Copy history cleared \n")
            pyperclip.copy("")

        time.sleep(0.1)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_commands)
    listener_thread.daemon = True
    listener_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")

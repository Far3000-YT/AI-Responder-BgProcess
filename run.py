# run.py
import time
import pyperclip
import keyboard
import os
import threading

from main.c_config import config as app_config
from main.a_config import send_to_gemini, configure_gemini_api_key, get_primary_api_key, get_secondary_api_key, get_api_key
from main.capture import take_screenshot, cleanup_screenshot
from main.status import is_busy, clear_status


bp = app_config.get("base_prompt")
dr = app_config.get("double_requests", False)
sc_cmd = app_config.get("screenshot_cmd")
cc_enabled = app_config.get("ctrl_c", True)
cooldown = app_config.get("cooldown_seconds", 5) # Adjusted default cooldown for clarity

current_api_key_index = 0
#lock for shared api key index
api_key_lock = threading.Lock()


def process_request_thread(image_path, initial_prompt):
    global current_api_key_index

    final_response = "Error processing request"
    used_key_index = 0
    is_processing_successful = False # Flag to track success

    try:
        selected_api_key = None
        with api_key_lock:
            if dr:
                #getting api key here based on current index
                used_key_index = current_api_key_index
                selected_api_key = get_api_key(used_key_index)
                #toggle index for next request
                current_api_key_index = 1 - current_api_key_index
                if selected_api_key:
                     print(f"Using {'Primary' if used_key_index == 0 else 'Secondary'} API key (Index {used_key_index})...")
                else:
                    #require both keys if dr is true, error if selected one missing
                    error_msg = f"API_KEY_ERROR: Key index {used_key_index} not set for double_requests."
                    print(f"Error: double_requests is true, but API key at index {used_key_index} is not set.")
                    final_response = error_msg
                    raise ValueError("API key missing for selected index")

            else: #double_requests is false
                used_key_index = 0
                selected_api_key = get_primary_api_key()
                if not selected_api_key:
                    error_msg = "API_KEY_ERROR: Primary key not set."
                    print("Error: No primary API key (GEMINI_KEY or API_KEY_GEMINI) is set.")
                    final_response = error_msg
                    raise ValueError("Primary API key missing")

        #configure api key for this request
        if not configure_gemini_api_key(selected_api_key):
             error_msg = f"API_CONFIG_ERROR: Could not configure API with key index {used_key_index}."
             final_response = error_msg
             raise RuntimeError("API configuration failed")

        print("Sending request to API...")
        #send request handling status internally
        api_response_text = send_to_gemini(image_path, initial_prompt)

        #check send_to_gemini error codes
        if api_response_text.startswith("API_REQUEST_ERROR"):
             print(f"API request failed: {api_response_text}")
             final_response = api_response_text
        elif api_response_text == "MODEL_INSTANCE_ERROR":
             print(f"API request failed: {api_response_text}")
             final_response = api_response_text
        elif api_response_text == "EMPTY_RESPONSE":
             print(f"API request returned empty response.")
             # Treat empty response as an error for clipboard purposes
             final_response = "Empty response from API."
        else:
            # Successful response from API
            final_response = api_response_text
            is_processing_successful = True # Mark as successful

    except Exception as e:
        print(f"An unexpected error occurred during request processing: {e}")
        #set specific error if default not overridden
        if final_response == "Error processing request":
            final_response = f"PROCESSING_ERROR: {type(e).__name__} - {e}"
        # Ensure flag is False on any exception
        is_processing_successful = False

    finally:
         #cleanup screenshot file regardless of success/failure
        cleanup_screenshot(image_path)

    # Copy the final result ONLY if processing was successful
    if is_processing_successful:
        try:
            pyperclip.copy(final_response)
            print("Response copied to clipboard.")
        except Exception as e:
             # Log if copying the successful response fails
             print(f"Error copying successful response to clipboard: {e}")
    else:
        # If it was an error, just print it to the console/log, don't copy to clipboard
        print(f"Processing completed with error/empty response, not copying to clipboard: {final_response}")


def listen_for_commands():
    print("AI Responder script running in background. Press configured hotkeys...")

    last_execution_time = 0

    while True:
        current_time = time.time()

        #skip checks if busy (based on .ai_status file)
        if is_busy():
             time.sleep(0.5) #check status less frequently to save cpu
             continue

        # --- Screenshot command ---
        if keyboard.is_pressed(sc_cmd):
            if current_time - last_execution_time >= cooldown:
                last_execution_time = current_time
                print(f"'{sc_cmd}' detected. Initiating screenshot process...")

                # Removed: No clipboard status update like "Capturing..."
                time.sleep(0.1) # Small delay might help ensure key release detection

                #blocking call waits for user points
                image_path = take_screenshot()

                if image_path:
                    print("Screenshot captured. Starting API processing...")
                    # Removed: No clipboard status update like "Processing..."

                    #start processing thread
                    process_thread = threading.Thread(
                        target=process_request_thread,
                        args=(image_path, bp)
                    )
                    process_thread.start()

                else:
                    # Screenshot cancelled or failed
                    print("Screenshot capture cancelled or failed.")
                    # Removed: No clipboard status update like "Capture failed"

            else:
                # Cooldown active
                remaining_time = int(cooldown - (current_time - last_execution_time))
                status_msg = f"Cooldown active. Wait {remaining_time}s"
                print(status_msg) # Log cooldown to console only
                # Removed: No clipboard status update for cooldown
                time.sleep(1) # Prevent spamming cooldown message log

        # --- Ctrl+C command ---
        if cc_enabled and keyboard.is_pressed('ctrl+c'):
             #debounce ctrl+c to allow clipboard update by system
             time.sleep(0.1)

             if current_time - last_execution_time >= cooldown:
                last_execution_time = current_time

                print("'Ctrl+C' detected. Processing clipboard text...")
                # Removed: No clipboard status update like "Processing..."

                #wait for clipboard update after system's ctrl+c action
                time.sleep(0.05)
                try:
                    text_input = pyperclip.paste()
                except Exception as e:
                     # Handle potential errors reading clipboard
                     print(f"Error reading clipboard: {e}")
                     text_input = "" # Treat as empty if read fails

                if not text_input:
                     # Clipboard empty or read error, do nothing further
                     print("Clipboard is empty or could not be read, nothing to process.")
                     # Removed: No clipboard status update like "Clipboard empty"
                     time.sleep(1) # Prevent spamming empty message logs
                     continue # Skip processing

                # If we got text, proceed
                print("Clipboard content read. Starting API processing...")

                combined_prompt = f"{text_input} \n {bp}"

                #start processing thread
                process_thread = threading.Thread(
                     target=process_request_thread,
                     args=("", combined_prompt) #no image path
                )
                process_thread.start()

             else:
                # Cooldown active
                remaining_time = int(cooldown - (current_time - last_execution_time))
                status_msg = f"Cooldown active. Wait {remaining_time}s"
                print(status_msg) # Log cooldown to console only
                # Removed: No clipboard status update for cooldown
                time.sleep(1) # Prevent spamming cooldown message log

        # --- Ctrl+V command (Clear Clipboard) --- remains as is
        if keyboard.is_pressed('ctrl+v'):
             print("Attempting to clear clipboard...")
             try:
                 time.sleep(0.05) #slight delay
                 # Check clipboard content before clearing (optional but good practice)
                 if pyperclip.paste() != "":
                     pyperclip.copy("") # Clear the clipboard
                     print("Clipboard cleared.")
                 else:
                      print("Clipboard already empty.")
                 time.sleep(0.5) #debounce clear action
             except Exception as e:
                 print(f"Error clearing clipboard: {e}")


        #prevent high cpu usage in listener loop
        time.sleep(0.03)

if __name__ == "__main__":
    print("Initializing AI Responder...")

    #initial cleanup
    clear_status()
    cleanup_screenshot(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp_screenshot.png"))

    #configure primary api key on startup
    primary_key = get_primary_api_key()
    if not primary_key:
         print("CRITICAL ERROR: Primary API key (GEMINI_KEY or API_KEY_GEMINI) not found.")
         print("Please set it in your .env file.")
         #exit if primary key missing
         exit(1)

    #configure primary key initially, thread logic re-configures per request
    if not configure_gemini_api_key(primary_key):
        print("CRITICAL ERROR: Initial API configuration failed with primary key.")
        exit(1)
    else:
         print("Initial API configuration successful.")
         if dr and not get_secondary_api_key():
              print("Warning: double_requests is True, but API_KEY_GEMINI2 is not set in environment.")
              print("Double request functionality will not work correctly without the secondary key.")

    #start listener thread
    #daemon thread allows main exit even if listener loop is active
    listener_thread = threading.Thread(target=listen_for_commands)
    listener_thread.daemon = True
    listener_thread.start()

    print("Script started. Waiting for commands...")

    #keep main thread alive for daemon listener
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user (KeyboardInterrupt).")
    except Exception as e:
         print(f"An unexpected error occurred in the main loop: {e}")
    finally:
        #cleanup on exit
        print("Shutting down...")
        clear_status()
        #note daemon threads may be killed abruptly if still running
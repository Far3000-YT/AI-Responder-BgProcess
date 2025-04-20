import os
import google.generativeai as genai
from PIL import Image

from .env import load_env
from .c_config import config as app_config
from .status import set_status, clear_status

load_env()

def configure_gemini_api_key(api_key):
    """configures the genai library globally with a specific api key"""
    if not api_key:
         print("Error: No API key provided for configuration.")
         return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring genai API key: {e}")
        return False

def get_api_key(use_key_index=0):
    """retrieves the api key string from environment variables based on index"""
    if use_key_index == 0:
        #prefer api_key_gemini over gemini_key
        return os.environ.get('API_KEY_GEMINI') or os.environ.get('GEMINI_KEY')
    elif use_key_index == 1:
        return os.environ.get('API_KEY_GEMINI2')
    else:
        print(f"Error: Invalid key index requested: {use_key_index}")
        return None


def get_gemini_model_instance():
    """returns a new gemini model instance configured from c_config"""
    mn = app_config.get("model_name", "gemini-1.5-flash-latest")
    mat = app_config.get("max_output_tokens", 8192)
    tk = app_config.get("top_k", 40)
    temp = app_config.get("temperature", 1.0)
    top_p = app_config.get("top_p", 0.95)

    generation_config = {
        "temperature": temp,
        "top_p": top_p,
        "top_k": tk,
        "max_output_tokens": mat,
        #assume text output
        "response_mime_type": "text/plain",
    }

    try:
        #key validity checked during generate_content, not here
        model = genai.GenerativeModel(model_name=mn, generation_config=generation_config)
        return model
    except Exception as e:
        print(f"Error creating Gemini model instance for {mn}: {e}")
        return None

def send_to_gemini(image_path, prompt):
    """sends a request to gemini using the currently configured api key"""
    model = get_gemini_model_instance()
    if not model:
         return "MODEL_INSTANCE_ERROR"

    set_status("loading")
    response_text = "API_REQUEST_FAILED"

    try:
        content = [prompt]
        if image_path:
            try:
                #image.open requires readable file
                image = Image.open(image_path)
                content.append(image)
            except Exception as img_e:
                 print(f"Error loading image {image_path}: {img_e}")
                 #proceed with text only if image load fails
                 print("Proceeding with text-only prompt due to image error.")

        #blocking api call
        response = model.generate_content(content)

        #accessing .text can raise errors on api failure
        response_text = response.text

        if not response_text:
             print("Warning: Received empty response text from API.")
             response_text = "EMPTY_RESPONSE"

    except Exception as e:
        print(f"API request error: {e}")
        #check for specific api errors like quota limits if needed
        response_text = f"API_REQUEST_ERROR: {type(e).__name__} - {e}"

    finally:
        clear_status()

    return response_text

#helpers for run.py key management
def get_primary_api_key():
    """helper to get the primary api key string"""
    return get_api_key(0)

def get_secondary_api_key():
     """helper to get the secondary api key string"""
     return get_api_key(1)
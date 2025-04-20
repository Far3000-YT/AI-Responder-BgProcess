import os
from dotenv import load_dotenv

def load_env():
    """loads environment variables from a .env file"""
    #expect .env in project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print(f"Warning: .env file not found at {dotenv_path}. API keys must be in system environment variables.")
import yaml
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

class AppConfig:
    """loads and holds application configuration from config.yaml"""
    def __init__(self, config_path=CONFIG_PATH):
        self.config = {}
        self._load_config(config_path)

    def _load_config(self, config_path):
        """loads configuration from the specified yaml file"""
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                self.config = yaml.safe_load(file)
            #handle empty config file
            if self.config is None:
                 self.config = {}
            print(f"Config loaded successfully from {config_path}.")
        except FileNotFoundError:
            print(f"Error: config file not found at {config_path}")
            #ensure config empty on load error
            self.config = {}
        except yaml.YAMLError as e:
            print(f"Error parsing config file {config_path}: {e}")
            self.config = {}

    def get(self, key, default=None):
        """gets a configuration value by key, returning default if not found"""
        return self.config.get(key, default)

#global configuration instance
config = AppConfig()
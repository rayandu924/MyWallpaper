import os
import json
import logging
import threading

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.lock = threading.Lock()  # Verrou global

    def load_config(self):
        with self.lock:  # Utiliser le verrou pour la lecture
            logging.info(f"Loading config from {self.config_file}")
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f).get("items", [])
                    logging.info(f"Config loaded: {config}")
                    return config
            except FileNotFoundError:
                logging.error(f"Config file not found at {self.config_file}")
                return []
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding config file: {e}")
                return []

    def save_config(self, config):
        with self.lock:  # Utiliser le verrou pour la sauvegarde
            try:
                logging.info(f"Saving config to {self.config_file}")
                with open(self.config_file, 'w') as f:
                    json.dump({"items": config}, f, indent=4)
                    logging.info("Config saved successfully.")
            except Exception as e:
                logging.error(f"Error saving config: {e}")
import logging
import json
from src.file_manager import FileManager

class JsonManager():
    @staticmethod
    def load_json(file_path):
        raw_data = FileManager.read_file(file_path)
        if raw_data is None:
            return {}
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {file_path}: {e}")
            return {}

    @staticmethod
    def save_json(file_path, data):
        try:
            json_data = json.dumps(data, indent=4)
            FileManager.write_file(file_path, json_data)
        except (TypeError, ValueError) as e:
            logging.error(f"Error encoding data to JSON for {file_path}: {e}")
import logging
import json
from src.file_manager import FileManager

class JsonManager:
    @staticmethod
    def parse_json(json_string):
        """
        Parse une chaîne JSON en objet Python (dictionnaire ou liste).
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON data: {e}")

    @staticmethod
    def load_json(file_path):
        """
        Charge un fichier JSON et retourne les données sous forme de dictionnaire.
        """
        raw_data = FileManager.read_file(file_path)
        if raw_data is None:
            return {}
        try:
            return JsonManager.parse_json(raw_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error loading JSON data from {file_path}: {e}")

    @staticmethod
    def save_json(file_path, data):
        """
        Sauvegarde les données sous forme de fichier JSON.
        """
        try:
            json_data = JsonManager.to_string(data)
            FileManager.write_file(file_path, json_data)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error saving JSON data to {file_path}: {e}")
    
    @staticmethod
    def to_string(data):
        """
        Convertit un objet Python en chaîne JSON.
        """
        try:
            return json.dumps(data, indent=4)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error converting data to JSON string: {e}")
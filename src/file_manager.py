import os
import json
import logging
import threading

class FileManager:
    @staticmethod
    def read_file(file_path):
        logging.info(f"Reading file from {file_path}")
        try:
            with open(file_path, 'r') as f:
                data = f.read()
                logging.info(f"File read successfully from {file_path}")
                return data
        except FileNotFoundError:
            logging.error(f"File not found at {file_path}")
            return None
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None
            
    @staticmethod
    def write_file(file_path, data):
        try:
            logging.info(f"Writing data to {file_path}")
            with open(file_path, 'w') as f:
                f.write(data)
                logging.info(f"Data written successfully to {file_path}")
        except Exception as e:
            logging.error(f"Error writing to file {file_path}: {e}")
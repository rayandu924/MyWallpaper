import os
import hashlib
import logging

class HashManager:
    def __init__(self, items_dir):
        self.items_dir = items_dir
        logging.info(f"Initializing HashManager for directory: {items_dir}")
        self.item_hashes = self.compute_hashes()

    def compute_hash(self, item_name):
        logging.info(f"Computing hash for item: {item_name}")
        item_path = os.path.join(self.items_dir, item_name)
        hash_md5 = hashlib.md5()
        try:
            for root, _, files in os.walk(item_path):
                for file in sorted(files):  # Sort files to ensure consistent hashing
                    file_path = os.path.join(root, file)
                    logging.info(f"Hashing file: {file_path}")
                    with open(file_path, "rb") as f:
                        while chunk := f.read(4096):
                            hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error computing hash for item {item_name}: {e}")
            return None

    def compute_hashes(self):
        logging.info("Computing hashes for all items.")
        item_hashes = {}
        all_items = self.list_items()
        for item in all_items:
            item_hashes[item] = self.compute_hash(item)
        return item_hashes

    def list_items(self):
        logging.info(f"Listing items in directory: {self.items_dir}")
        return [d for d in os.listdir(self.items_dir) if os.path.isdir(os.path.join(self.items_dir, d))]

    def update_hash(self, item_name):
        logging.info(f"Updating hash for item: {item_name}")
        new_hash = self.compute_hash(item_name)
        if new_hash:
            self.item_hashes[item_name] = new_hash

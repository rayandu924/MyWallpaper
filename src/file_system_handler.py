import os
import logging
from watchdog.events import FileSystemEventHandler

class FileSystemHandler(FileSystemEventHandler):
    def __init__(self, config_manager, hash_manager, reinjection_callback):
        self.config_manager = config_manager
        self.hash_manager = hash_manager
        self.reinjection_callback = reinjection_callback
        logging.info("FileSystemHandler initialized.")

    def on_modified(self, event):
        logging.info(f"Modification detected: {event.src_path}")
        if event.is_directory:
            logging.info("Modification is a directory, ignoring.")
            return

        # Vérifiez si le fichier modifié est un fichier `index.html`
        if os.path.basename(event.src_path) == "index.html":
            # Obtenir le nom du dossier parent
            addon_name = os.path.basename(os.path.dirname(event.src_path))
            logging.info(f"Addon modified: {addon_name}. Re-checking configuration for item-specific update.")
            self.reinjection_callback([addon_name])
        elif event.src_path == self.config_manager.config_file:
            logging.info("Configuration file modified. Re-checking configuration.")
            new_config = self.config_manager.load_config()
            self.reinjection_callback(new_config)


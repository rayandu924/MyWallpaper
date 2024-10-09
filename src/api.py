from PyQt5.QtCore import QObject, pyqtSlot
import logging
import os

class Api(QObject):
    def __init__(self, wallpaper_manager=None):
        super().__init__()
        self.wallpaper_manager = wallpaper_manager

    @pyqtSlot(result=str)
    def get_config(self):
        # Retourne la configuration des items (exemple simple)
        return '{"items": [{"name": "item1", "enabled": true, "position": 1}]}'

    @pyqtSlot(str, str)
    def save_item_config(self, item_name, new_config):
        # Simule la sauvegarde de la configuration d'un item
        logging.info(f"Saving config for {item_name}: {new_config}")

        # Appeler la mise à jour dans le WallpaperManager
        if self.wallpaper_manager:
            self.wallpaper_manager.update_item(item_name, new_config)

        return "Configuration saved!"

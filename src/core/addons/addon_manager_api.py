import json
from .addon_manager import AddonManager

class AddonManagerAPI:
    def __init__(self, addons_dir):
        self.addon_manager = AddonManager(addons_dir)

    def get_addons(self):
        """Renvoie la liste des addons disponibles."""
        return self.addon_manager.get_addons_list()

    def load_config(self, addon_name):
        """Charge la configuration JSON d'un addon spécifique."""
        config = self.addon_manager.get_config(addon_name)
        return config

    def save_config(self, addon_name, config):
        """Sauvegarde la configuration mise à jour d'un addon."""
        self.addon_manager.save_config(addon_name, config)
        return {"status": "success"}

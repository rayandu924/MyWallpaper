import json
from .addon_manager import AddonManager

class AddonManagerAPI:
    def __init__(self, addons_dir):
        self.addon_manager = AddonManager(addons_dir)

    def get_addons(self):
        """Returns the list of available addons."""
        return self.addon_manager.get_addons_list()

    def load_config(self, addon_name):
        """Loads the configuration JSON of a specific addon."""
        config = self.addon_manager.get_config(addon_name)
        return config

    def save_config(self, addon_name, config):
        """Saves the updated configuration of an addon."""
        self.addon_manager.save_config(addon_name, config)
        return {"status": "success"}

    def save_addon_order(self, order):
        """Saves the new order of addons."""
        self.addon_manager.save_order(order)
        return {"status": "success"}

import os
import logging

class Updater:
    def __init__(self, injector, config_manager):
        self.injector = injector
        self.config_manager = config_manager
        self.config = self.config_manager.load_config()
        logging.info("Updater initialized.")

    def update_items(self, modified_items):
        logging.info("Updating specific items.")
        for item_name in modified_items:
            logging.info(f"Updating item: {item_name}")
            matching_item = self.get_matching_item(item_name)
            if matching_item:
                self.update_item(matching_item)
            else:
                self.remove_item(item_name)

    def get_matching_item(self, item_name):
        logging.info(f"Checking configuration for item: {item_name}")
        return next((item for item in self.config if item["name"] == item_name and item.get("enabled", False)), None)

    def update_item(self, item):
        logging.info(f"Injecting content for item: {item['name']}")
        addon_path = os.path.join(os.path.dirname(self.config_manager.config_file), item['name'], "index.html")
        print(f"position: {item.get('position')}")
        self.injector.inject_content(item['name'], addon_path, item.get("position"))

    def remove_item(self, item_name):
        logging.info(f"Removing content for item: {item_name}")
        self.injector.remove_content(item_name)
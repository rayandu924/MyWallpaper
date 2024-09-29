import os
import json
import logging

class AddonManager:
    """Manages the list of addons and their configuration."""
    def __init__(self, addons_dir):
        self.addons_dir = addons_dir

    def get_addons_list(self):
        """Returns the list of valid addon directories."""
        logging.info(f"Searching for addons in: {self.addons_dir}")
        addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]
        logging.info(f"Found addons: {addons}")
        return addons

    def get_config(self, addon_name):
        """Returns the configuration of an addon from the index.html file."""
        config_path = os.path.join(self.addons_dir, addon_name, 'index.html')
        logging.info(f"Loading configuration for addon: {addon_name} from {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
                end = content.find('</script>', start)
                json_str = content[start:end]
                logging.info(f"Loaded configuration: {json_str}")
                return json.loads(json_str)
        except Exception as e:
            logging.error(f"Error loading configuration for addon {addon_name}: {e}")
            return None

    def save_config(self, addon_name, config):
        """Saves the updated configuration to the index.html file."""
        config_path = os.path.join(self.addons_dir, addon_name, 'index.html')
        logging.info(f"Saving new configuration for addon: {addon_name} to {config_path}")

        try:
            with open(config_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
                end = content.find('</script>', start)

                new_content = content[:start] + json.dumps(config, indent=4) + content[end:]
                f.seek(0)
                f.write(new_content)
                f.truncate()
                logging.info(f"Configuration successfully saved for addon: {addon_name}")
        except Exception as e:
            logging.error(f"Error saving configuration for addon {addon_name}: {e}")

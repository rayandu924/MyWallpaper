import os
import json
import logging

class AddonManager:
    """Manages the list of addons and their configuration."""
    
    def __init__(self, addons_dir):
        self.addons_dir = addons_dir
        self.config_file = os.path.join(addons_dir, 'config.json')
        self.load_order()

    def load_order(self):
        """Load the saved addon order from config.json."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.addon_order = json.load(f)
        else:
            self.addon_order = []

    def save_order(self, order):
        """Save the new addon order to config.json."""
        self.addon_order = order
        with open(self.config_file, 'w') as f:
            json.dump(order, f)

    def get_addons_list(self):
        """Returns the list of valid addon directories in saved order."""
        addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]
        ordered_addons = [addon for addon in self.addon_order if addon in addons]
        unordered_addons = [addon for addon in addons if addon not in ordered_addons]
        return ordered_addons + unordered_addons

    def get_config(self, addon_name):
        """Returns the configuration of an addon from the index.html file."""
        config_path = os.path.join(self.addons_dir, addon_name, 'index.html')

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
                end = content.find('</script>', start)
                json_str = content[start:end]
                return json.loads(json_str)
        except Exception as e:
            logging.error(f"Error loading configuration for addon {addon_name}: {e}")
            return None

    def save_config(self, addon_name, updated_config):
        """Saves the updated configuration to the index.html file."""
        config_path = os.path.join(self.addons_dir, addon_name, 'index.html')

        try:
            with open(config_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
                end = content.find('</script>', start)

                # Load the current config, update only the relevant parts
                current_config = json.loads(content[start:end])
                current_config.update(updated_config)  # Only update the changed values

                # Write the new configuration back to the file
                new_content = content[:start] + json.dumps(current_config, indent=4) + content[end:]
                f.seek(0)
                f.write(new_content)
                f.truncate()
        except Exception as e:
            logging.error(f"Error saving configuration for addon {addon_name}: {e}")

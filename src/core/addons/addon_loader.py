import os
import json
import logging
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigEventHandler(FileSystemEventHandler):
    """Handles changes to config.json."""
    def __init__(self, addon_loader):
        self.addon_loader = addon_loader

    def on_modified(self, event):
        if event.src_path.endswith("config.json"):
            logging.info("Detected change in config.json, reloading addons...")
            self.addon_loader.load_and_inject_addons()

class AddonLoader:
    """Loads and injects addon content into the web view."""
    def __init__(self, wallpaper, addons_dir):
        self.wallpaper = wallpaper
        self.addons_dir = addons_dir
        self.config_file = os.path.join(addons_dir, 'config.json')
        self.addon_order = self.load_addon_order()

        # Start watching for changes in config.json
        self.start_watching_config()

    def start_watching_config(self):
        """Start watching config.json for changes."""
        event_handler = ConfigEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, self.addons_dir, recursive=False)
        observer.start()

    def load_addon_order(self):
        """Loads the order of addons from config.json."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    addon_order = json.load(f)
                logging.info(f"Loaded addon order: {addon_order}")
                return addon_order
            except Exception as e:
                logging.error(f"Failed to load addon order: {e}")
                return []
        else:
            logging.warning(f"No config.json found. Addons will be loaded in default order.")
            return []

    def load_and_inject_addons(self):
        """Reload and inject addons according to the updated order."""
        self.addon_order = self.load_addon_order()
        self.inject_addons()

    def inject_addons(self):
        """Inject all valid addons into the web view in the specified order."""
        if not os.path.exists(self.addons_dir):
            logging.error(f"Addons directory does not exist: {self.addons_dir}")
            return

        # Get list of all addons
        all_addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]

        # Sort addons based on the order in config.json
        ordered_addons = [addon for addon in self.addon_order if addon in all_addons]
        unordered_addons = [addon for addon in all_addons if addon not in ordered_addons]

        # Remove all current iframes
        self.remove_all_iframes()

        # Inject addons in the specified order
        for addon_name in ordered_addons + unordered_addons:
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                self.inject_html_content(addon_name, addon_path)

    def remove_all_iframes(self):
        """Remove all iframes from the web view."""
        script = """
        var iframes = document.querySelectorAll('iframe');
        iframes.forEach(function(iframe) {
            iframe.remove();
        });
        """
        self.wallpaper.page().runJavaScript(script)

    def inject_html_content(self, addon_name, addon_path):
        """Inject an iframe for the addon."""
        script = f"""
        var iframe = document.createElement('iframe');
        iframe.setAttribute('addon', '{addon_name}');
        iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';
        document.body.appendChild(iframe);
        """
        self.wallpaper.page().runJavaScript(script)

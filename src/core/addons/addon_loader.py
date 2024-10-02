import os
import json
import logging
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AddonLoader(FileSystemEventHandler):
    """Loads and injects addon content into the web view, with monitoring for changes."""
    
    def __init__(self, wallpaper, addons_dir):
        self.wallpaper = wallpaper
        self.addons_dir = addons_dir
        self.config_file = os.path.join(addons_dir, 'config.json')
        self.addon_order = self.load_addon_order()
        self.observer = Observer()
        self.start_watching()

    def start_watching(self):
        """Start watching the addon directory for changes."""
        self.observer.schedule(self, self.addons_dir, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        """Handles any modification event in the addon directory."""
        # Extract addon name from the modified file path
        if event.is_directory:
            addon_name = os.path.basename(event.src_path)
        else:
            addon_name = os.path.basename(os.path.dirname(event.src_path))

        logging.info(f"Detected change in addon folder: {addon_name}, reinjecting...")
        self.reinject_addon(addon_name)

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

        # Inject addons in the specified order
        for addon_name in ordered_addons + unordered_addons:
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                self.inject_html_content(addon_name, addon_path)

    def reinject_addon(self, addon_name):
        """Reinject the iframe for a specific addon while keeping its position."""
        addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
        if os.path.exists(addon_path):
            # Find the iframe and its position in the DOM
            script_find_position = f"""
            (function() {{
                var iframe = document.querySelector('iframe[addon="{addon_name}"]');
                if (iframe) {{
                    var position = Array.from(document.body.children).indexOf(iframe);
                    iframe.remove();
                    return position;
                }} else {{
                    return -1;
                }}
            }})();
            """
            
            # Execute the JavaScript and capture the position
            def handle_position(pos):
                if pos is None or pos == -1:
                    pos = 'null'
                self.inject_html_content(addon_name, addon_path, pos)
            
            self.wallpaper.page().runJavaScript(script_find_position, handle_position)

    def inject_html_content(self, addon_name, addon_path, position=None):
        """Inject an iframe for the addon at a specific position."""
        position = 'null' if position is None else position  # Ensure position is null in JS when not set
        
        script = f"""
        // Remove any existing iframe with the same addon attribute
        var existingIframe = document.querySelector('iframe[addon="{addon_name}"]');
        if (existingIframe) {{
            existingIframe.remove();
        }}

        // Create and inject the new iframe
        var iframe = document.createElement('iframe');
        iframe.setAttribute('addon', '{addon_name}');
        iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';

        if ({position} !== null) {{
            var referenceNode = document.body.children[{position}];
            document.body.insertBefore(iframe, referenceNode);
        }} else {{
            document.body.appendChild(iframe);
        }}
        """
        self.wallpaper.page().runJavaScript(script)

    def stop_watching(self):
        """Stop the observer when shutting down."""
        self.observer.stop()
        self.observer.join()

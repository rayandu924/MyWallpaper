import os
import json
import logging
from PyQt5.QtCore import QUrl, QThreadPool, QRunnable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib

class AddonLoader(FileSystemEventHandler):
    """Loads and injects addon content into the web view, with monitoring for changes."""
    
    def __init__(self, wallpaper, addons_dir):
        self.wallpaper = wallpaper
        self.addons_dir = addons_dir
        self.config_file = os.path.join(addons_dir, 'config.json')
        self.addon_order = self.load_addon_order()
        self.addon_hashes = self.compute_addon_hashes()  # Initialiser les hashes des addons
        self.addon_injection_locked = False  # Flag to lock injection
        self.observer = Observer()
        self.start_watching()
        self.inject_addons()
        
    def start_watching(self):
        """Start watching the addon directory for changes."""
        self.observer.schedule(self, self.addons_dir, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        """Handles any modification event in the addon directory."""
        if event.is_directory:
            return

        # If config.json is modified, reposition if necessary
        if event.src_path == self.config_file:
            logging.info("config.json modified. Checking addon positions.")
            self.reposition_iframes()
        else:
            addon_name = os.path.basename(os.path.dirname(event.src_path))
            new_hash = self.compute_addon_hash(addon_name)
            
            # Only reinject if the addon content has actually changed
            if addon_name in self.addon_hashes and self.addon_hashes[addon_name] != new_hash:
                logging.info(f"Detected change in addon: {addon_name}. Reinjecting addon...")
                self.addon_hashes[addon_name] = new_hash
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

    def compute_addon_hashes(self):
        """Compute initial hashes for all addons to detect future changes."""
        addon_hashes = {}
        all_addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]
        for addon in all_addons:
            addon_hashes[addon] = self.compute_addon_hash(addon)
        return addon_hashes

    def compute_addon_hash(self, addon_name):
        """Compute a hash for the addon files to detect changes."""
        addon_path = os.path.join(self.addons_dir, addon_name)
        hash_md5 = hashlib.md5()
        try:
            for root, dirs, files in os.walk(addon_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        while chunk := f.read(4096):
                            hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error computing hash for addon {addon_name}: {e}")
            return None

    def inject_addons(self):
        """Inject all valid addons into the web view in the specified order."""
        logging.info("Injecting addons in the initial order.")
        self.addon_order = self.load_addon_order()  # Ensure the addon order is loaded

        all_addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]

        # Sort addons based on the order in config.json
        ordered_addons = [addon for addon in self.addon_order if addon in all_addons]
        unordered_addons = [addon for addon in all_addons if addon not in ordered_addons]

        for position, addon_name in enumerate(ordered_addons + unordered_addons):
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                self.inject_html_content(addon_name, addon_path, position)

    def reinject_addon(self, addon_name):
            """Reinject the iframe for a specific addon while keeping its position."""
            if self.addon_injection_locked:
                return  # Skip reinjection if another one is still in progress
            
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                def handle_position(pos):
                    if pos is None or pos == -1:
                        pos = 'null'
                    self.inject_html_content(addon_name, addon_path, pos)
                
                # Find the current position of the iframe and reinject it
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
                self.wallpaper.page().runJavaScript(script_find_position, handle_position)
            
    def inject_html_content(self, addon_name, addon_path, position=None):
        """Inject an iframe for the addon at a specific position."""
        # Lock injection to prevent race conditions
        if self.addon_injection_locked:
            return
        self.addon_injection_locked = True

        # Ensure position is null in JS when not set
        position = 'null' if position is None else position
        
        script = f"""
        // Remove any existing iframe with the same addon attribute
        var existingIframe = document.querySelector('iframe[addon="{addon_name}"]');
        var position = {position};
        
        if (existingIframe) {{
            position = Array.from(document.body.children).indexOf(existingIframe);
            existingIframe.remove();
        }}

        // Create and inject the new iframe at the stored position
        var iframe = document.createElement('iframe');
        iframe.setAttribute('addon', '{addon_name}');
        iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';

        if (position !== null && position >= 0 && position < document.body.children.length) {{
            var referenceNode = document.body.children[position];
            document.body.insertBefore(iframe, referenceNode);
        }} else {{
            document.body.appendChild(iframe);
        }}
        """
        
        def handle_injection_finished(result):
            # Release lock after the injection finishes
            self.addon_injection_locked = False
        
        # Run the script and release lock when finished
        self.wallpaper.page().runJavaScript(script, handle_injection_finished)

    def reposition_iframes(self):
        """Reposition the iframes according to the updated order in config.json."""
        new_addon_order = self.load_addon_order()
        if new_addon_order == self.addon_order:
            logging.info("Addon order hasn't changed. No need to reposition.")
            return

        self.addon_order = new_addon_order
        self.reposition_addons()

    def reposition_addons(self):
        """Reposition all addons' iframes based on the order in config.json."""
        logging.info("Repositioning addons...")
        all_addons = [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]

        # Sort addons based on the new order in config.json
        ordered_addons = [addon for addon in self.addon_order if addon in all_addons]
        unordered_addons = [addon for addon in all_addons if addon not in ordered_addons]

        # Inject addons in the specified order
        for position, addon_name in enumerate(ordered_addons + unordered_addons):
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                self.reposition_iframe(addon_name, addon_path, position)

    def reposition_iframe(self, addon_name, addon_path, position):
        """Reposition an iframe based on the new position."""
        script_reposition = f"""
        (function() {{
            var existingIframe = document.querySelector('iframe[addon="{addon_name}"]');
            if (existingIframe) {{
                existingIframe.remove();
            }}

            var iframe = document.createElement('iframe');
            iframe.setAttribute('addon', '{addon_name}');
            iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';

            var referenceNode = document.body.children[{position}];
            if (referenceNode) {{
                document.body.insertBefore(iframe, referenceNode);
            }} else {{
                document.body.appendChild(iframe);
            }}
        }})();
        """
        self.wallpaper.page().runJavaScript(script_reposition)
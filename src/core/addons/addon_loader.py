import os
import json
import logging
import hashlib
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class AddonLoader(FileSystemEventHandler):
    """Loads and injects addon content into the web view, with monitoring for changes."""

    def __init__(self, wallpaper, addons_dir):
        self.wallpaper = wallpaper
        self.addons_dir = addons_dir
        self.config_file = os.path.join(addons_dir, 'config.json')
        self.addon_order = self.load_addon_order()
        self.addon_hashes = self.compute_addon_hashes()
        self.injection_lock = threading.Lock()  # Use threading lock
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

        if event.src_path == self.config_file:
            logging.info("config.json modified. Checking addon positions.")
            self.reposition_iframes()
        else:
            addon_name = os.path.basename(os.path.dirname(event.src_path))
            new_hash = self.compute_addon_hash(addon_name)

            if addon_name in self.addon_hashes and self.addon_hashes[addon_name] != new_hash:
                logging.info(f"Detected change in addon: {addon_name}. Reinjecting addon...")
                self.addon_hashes[addon_name] = new_hash
                self.reinject_addon(addon_name)

    def load_addon_order(self):
        """Loads the order of addons from config.json, or return an empty list if not found."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding config.json: {e}")
            except Exception as e:
                logging.error(f"Error loading config.json: {e}")
        else:
            logging.warning("No config.json found. Using default order.")
        return []

    def compute_addon_hashes(self):
        """Compute initial hashes for all addons to detect future changes."""
        addon_hashes = {}
        all_addons = self.list_addons()
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

    def list_addons(self):
        """Return a list of all addon directories."""
        return [d for d in os.listdir(self.addons_dir) if os.path.isdir(os.path.join(self.addons_dir, d))]

    def inject_addons(self):
        """Inject all valid addons into the web view in the specified order."""
        logging.info("Injecting addons in the initial order.")
        self.process_addons(self.inject_iframe)

    def reinject_addon(self, addon_name):
        """Reinject a specific addon iframe."""
        if not self.injection_lock.acquire(blocking=False):
            return  # Skip reinjection if another one is still in progress

        addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
        if os.path.exists(addon_path):
            self.get_iframe_position(addon_name, lambda pos: self.inject_iframe(addon_name, addon_path, pos))
        else:
            self.injection_lock.release()

    def inject_iframe(self, addon_name, addon_path, position=None):
        """Inject an iframe for the addon at a specific position."""
        script = f"""
        var existingIframe = document.querySelector('iframe[addon="{addon_name}"]');
        var position = {position if position is not None else 'null'};

        if (existingIframe) {{
            position = Array.from(document.body.children).indexOf(existingIframe);
            existingIframe.remove();
        }}

        var iframe = document.createElement('iframe');
        iframe.setAttribute('addon', '{addon_name}');
        iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';

        if (position !== null && position >= 0 && position < document.body.children.length) {{
            document.body.insertBefore(iframe, document.body.children[position]);
        }} else {{
            document.body.appendChild(iframe);
        }}
        """

        def on_javascript_execution(result):
            with self.injection_lock:  # Release the lock in a context manager
                pass

        self.wallpaper.page().runJavaScript(script, on_javascript_execution)

    def get_iframe_position(self, addon_name, callback):
        """Find the position of the iframe and invoke a callback with the position."""
        script = f"""
        (function() {{
            var iframe = document.querySelector('iframe[addon="{addon_name}"]');
            if (iframe) {{
                var position = Array.from(document.body.children).indexOf(iframe);
                iframe.remove();
                return position;
            }}
            return -1;
        }})();
        """
        self.wallpaper.page().runJavaScript(script, callback)

    def reposition_iframes(self):
        """Reposition the iframes according to the updated order in config.json."""
        new_addon_order = self.load_addon_order()
        if new_addon_order != self.addon_order:
            self.addon_order = new_addon_order
            self.process_addons(self.inject_iframe)

    def process_addons(self, action):
        """Process and apply an action (like injection or repositioning) to addons."""
        all_addons = self.list_addons()
        ordered_addons = [addon for addon in self.addon_order if addon in all_addons]
        unordered_addons = [addon for addon in all_addons if addon not in ordered_addons]

        for position, addon_name in enumerate(ordered_addons + unordered_addons):
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                action(addon_name, addon_path, position)

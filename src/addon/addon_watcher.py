from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import time

class AddonWatcher(FileSystemEventHandler):
    def __init__(self, addon_loader, addons_dir, extensions=None):
        self.addon_loader = addon_loader
        self.addons_dir = addons_dir
        self.extensions = extensions if extensions is not None else ['.html', '.js']
        self.last_modified = time.time()  # Track the last modification time

    def on_modified(self, event):
        if event.is_directory:
            return
        
        current_time = time.time()

        # Debounce: Ignore events if they occur within a short interval (e.g., 1 second)
        if current_time - self.last_modified < 1:
            return

        if any(event.src_path.endswith(ext) for ext in self.extensions):
            print(f"File modified: {event.src_path}. Reloading addon.")
            self.addon_loader.inject_addons(self.addons_dir)  # Reinject the modified addon

        self.last_modified = current_time

def start_addon_watcher(addon_loader, addons_dir, extensions=None):
    event_handler = AddonWatcher(addon_loader, addons_dir, extensions)
    observer = Observer()
    observer.schedule(event_handler, path=addons_dir, recursive=True)
    observer.start()
    return observer

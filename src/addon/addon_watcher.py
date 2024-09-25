from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os

class AddonWatcher(FileSystemEventHandler):
    def __init__(self, addon_loader, addons_dir, extensions=None):
        self.addon_loader = addon_loader
        self.addons_dir = addons_dir
        self.extensions = extensions if extensions is not None else ['.html', '.js']

    def on_modified(self, event):
        if event.is_directory:
            return
        if any(event.src_path.endswith(ext) for ext in self.extensions):
            print(f"File modified: {event.src_path}. Reloading addons.")
            self.addon_loader.inject_addons(self.addons_dir)

def start_addon_watcher(addon_loader, addons_dir, extensions=None):
    event_handler = AddonWatcher(addon_loader, addons_dir, extensions)
    observer = Observer()
    observer.schedule(event_handler, path=addons_dir, recursive=True)
    observer.start()
    return observer

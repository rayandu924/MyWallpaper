from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class AddonWatcher(FileSystemEventHandler):
    """Watcher to monitor changes in the addons directory and reload addons."""
    
    def __init__(self, addon_loader):
        self.addon_loader = addon_loader

    def on_any_event(self, event):
        if event.event_type in {'modified', 'created', 'moved', 'deleted'}:
            print(f"Change detected: {event.src_path}. Reloading addons.")
            self.addon_loader.inject_addons()

def start_addon_watcher(addon_loader):
    """Starts the filesystem observer to watch for changes in the addons directory."""
    
    event_handler = AddonWatcher(addon_loader)
    observer = Observer()
    observer.schedule(event_handler, path=addon_loader.addons_dir, recursive=True)
    observer.start()
    
    print(f"Started watching {addon_loader.addons_dir} for changes.")
    
    return observer

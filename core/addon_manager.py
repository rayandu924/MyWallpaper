import os
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AddonLoader:
    def __init__(self, web_view):
        self.web_view = web_view

    def inject_addons(self, addons_dir):
        if not os.path.exists(addons_dir):
            print(f"Addons directory does not exist: {addons_dir}")
            return

        addon_files = self.get_addon_files(addons_dir)
        for addon_name, addon_url in addon_files:
            self.update_or_inject_iframe(addon_url, addon_name)

    def get_addon_files(self, addons_dir):
        addon_files = []
        for addon_name in os.listdir(addons_dir):
            addon_path = os.path.join(addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                addon_url = QUrl.fromLocalFile(os.path.abspath(addon_path))
                addon_files.append((addon_name, addon_url))
        return addon_files

    def update_or_inject_iframe(self, addon_url, addon_name):
        script = f'''
        var iframe = document.getElementById("{addon_name}_iframe");
        if (iframe) {{
            iframe.src = "{addon_url.toString()}";
        }} else {{
            iframe = document.createElement('iframe');
            iframe.id = "{addon_name}_iframe";
            iframe.src = "{addon_url.toString()}";
            iframe.style.position = "absolute";
            iframe.style.top = "0";
            iframe.style.left = "0";
            iframe.style.width = "100vw";
            iframe.style.height = "100vh";
            iframe.style.border = "none";
            document.body.appendChild(iframe);
        }}
        '''
        self.web_view.page().runJavaScript(script)

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

def start_watching(addon_loader, addons_dir, extensions=None):
    event_handler = AddonWatcher(addon_loader, addons_dir, extensions)
    observer = Observer()
    observer.schedule(event_handler, path=addons_dir, recursive=True)
    observer.start()
    return observer
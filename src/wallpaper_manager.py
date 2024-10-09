import ctypes
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from src.json_manager import JsonManager
from src.item_manager import ItemManager
from src.app_manager import AppManager

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, manager):
        self.manager = manager

    def on_modified(self, event):
        logging.info(f"File modified: {event.src_path}")
        # Recharger la page quand un fichier est modifié
        self.manager.reload_page()

class WallpaperManager(QMainWindow):
    user32 = ctypes.windll.user32

    def __init__(self):
        super().__init__()
        self.wallpaper = Path('src/ui/wallpaper/index.html').resolve()
        self.setup_ui()
        self.set_as_wallpaper(int(self.winId()))
        self.open_devtools()

        # Surveiller le dossier 'items' pour des changements
        self.start_file_observer()

    def setup_ui(self):
        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl.fromLocalFile(self.wallpaper.as_posix()))
        self.showFullScreen()
        self.setCentralWidget(self.web_view)
        self.web_view.loadFinished.connect(self.on_page_load_finished)

    def open_devtools(self):
        logging.info("Opening DevTools.")
        dev_tools_view = QWebEngineView(self)
        dev_tools_page = QWebEnginePage(self.web_view)
        self.web_view.page().setDevToolsPage(dev_tools_page)
        dev_tools_view.setPage(dev_tools_page)
        self.devtools_window = QMainWindow(self)
        self.devtools_window.setCentralWidget(dev_tools_view)
        self.devtools_window.show()

    def on_page_load_finished(self):
        logging.info("Main page load finished. Setting up item handlers.")
        addons_dir = Path('items/').resolve()
        config_file = os.path.join(addons_dir, 'config.json')
        config = JsonManager.load_json(config_file)
        ItemManager.update_items(self.web_view, config.get("items"))

    def reload_page(self):
        addons_dir = Path('items/').resolve()
        config_file = os.path.join(addons_dir, 'config.json')
        config = JsonManager.load_json(config_file)
        ItemManager.update_items(self.web_view, config.get("items"))
        ItemManager.update_items(self.web_view, config.get("items"))

    def start_file_observer(self):
        logging.info("Starting file observer for the 'items' directory.")
        event_handler = FileChangeHandler(self)
        observer = Observer()
        items_dir = Path('items/').resolve()

        observer.schedule(event_handler, str(items_dir), recursive=True)
        observer_thread = threading.Thread(target=observer.start)
        observer_thread.start()

        # Assurer que l'observateur s'arrête avec l'application
        self.observer = observer
        self.observer_thread = observer_thread

    def closeEvent(self, event):
        # Arrêter l'observateur lorsque la fenêtre se ferme
        logging.info("Stopping file observer.")
        self.observer.stop()
        self.observer.join()
        
    @staticmethod
    def set_as_wallpaper(window_id):
        logging.info(f"Setting window {window_id} as wallpaper.")
        progman = WallpaperManager.user32.FindWindowW("Progman", None)
        WallpaperManager.user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, None)
        WallpaperManager.user32.SetParent(window_id, progman)

def start_wallpaper_app():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting application.")
    app = QApplication([])
    wallpaper_app = WallpaperManager()
    wallpaper_app.show()
    app.exec_()

if __name__ == "__main__":
    wallpaper_thread = threading.Thread(target=start_wallpaper_app)
    wallpaper_thread.start()
    AppManager.create_app()
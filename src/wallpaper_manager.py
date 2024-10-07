import ctypes
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl
from src.json_manager import JsonManager
from src.item_manager import ItemManager

class WallpaperManager(QMainWindow):
    user32 = ctypes.windll.user32

    def __init__(self):
        super().__init__()
        self.wallpaper = Path('src/ui/wallpaper/index.html').resolve()
        self.setup_ui()
        self.set_as_wallpaper(int(self.winId()))
        self.open_devtools()

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
        
        addons_dir = Path('addons/').resolve()
        config_file = os.path.join(addons_dir, 'config.json')
        
        config = JsonManager.load_json(config_file)
        ItemManager.update_items(self.web_view, config.get("items"))
        

    @staticmethod
    def set_as_wallpaper(window_id):
        logging.info(f"Setting window {window_id} as wallpaper.")
        try:
            progman = WallpaperManager.find_progman()
            WallpaperManager.send_message_to_progman(progman)
            WallpaperManager.set_window_as_child(window_id, progman)
        except (RuntimeError, ValueError) as e:
            logging.error(f"Error setting wallpaper: {e}")
            raise

    @staticmethod
    def find_progman():
        logging.info("Attempting to find Progman window...")
        try:
            progman = WallpaperManager.user32.FindWindowW("Progman", None)
            if not progman:
                raise RuntimeError("Progman window not found.")
            logging.info(f"Progman window found: {progman}")
        except RuntimeError as e:
            logging.error(f"Error finding Progman: {e}")
            raise
        return progman

    @staticmethod
    def send_message_to_progman(progman):
        logging.info("Sending message to Progman to prepare wallpaper...")
        if not progman:
            raise ValueError("Invalid Progman window handle.")
        try:
            result = WallpaperManager.user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, None)
            if result == 0:
                raise RuntimeError("Failed to send message to Progman.")
            logging.info("Message sent to Progman successfully.")
        except (ValueError, RuntimeError) as e:
            logging.error(f"Error sending message to Progman: {e}")
            raise
        return True

    @staticmethod
    def set_window_as_child(window_id, progman):
        logging.info(f"Setting window {window_id} as child of Progman...")
        if not window_id:
            raise ValueError("Invalid window handle.")
        if not progman:
            raise ValueError("Progman window handle is not set.")
        try:
            set_parent_result = WallpaperManager.user32.SetParent(window_id, progman)
            if set_parent_result == 0:
                raise RuntimeError("Failed to set window as child of Progman.")
            logging.info("Window set as child of Progman successfully.")
        except (ValueError, RuntimeError) as e:
            logging.error(f"Error setting window as child of Progman: {e}")
            raise
        return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting application.")
    app = QApplication([])
    wallpaper_app = WallpaperManager()
    wallpaper_app.show()
    app.exec_()
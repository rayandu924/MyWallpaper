import ctypes
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
import threading
from src.wallpaper_manager_api import start_api

class WallpaperManager(QMainWindow):
    user32 = ctypes.windll.user32

    def __init__(self):
        super().__init__()
        self.wallpaper = Path('src/static/wallpaper/index.html').resolve()
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

    @staticmethod
    def set_as_wallpaper(window_id):
        logging.info(f"Setting window {window_id} as wallpaper.")
        progman = WallpaperManager.user32.FindWindowW("Progman", None)
        WallpaperManager.user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, None)
        WallpaperManager.user32.SetParent(window_id, progman)

    def on_page_load_finished(self):
        logging.info("Page loaded successfully.")
        # You can now modify the web_view here or through API

def start_wallpaper_app():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting application.")
    
    app = QApplication([])  
    wallpaper_app = WallpaperManager()
    wallpaper_app.show()
    
    # Démarrer l'API dans un thread séparé
    api_thread = threading.Thread(target=start_api, args=(wallpaper_app,), daemon=True)
    api_thread.start()


    app.exec_()

if __name__ == "__main__":
    start_wallpaper_app()

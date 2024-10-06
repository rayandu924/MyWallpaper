import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl
from src.config_manager import ConfigManager
from src.hash_manager import HashManager
from src.wallpaper_manager import WallpaperManager
from src.file_system_handler import FileSystemHandler
from src.injector import Injector
from src.updater import Updater
from watchdog.observers import Observer

class WallpaperLauncher(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()
        logging.info("Initializing WallpaperLauncher.")
        self.wallpaper = Path('src/ui/wallpaper/index.html').resolve()

        # Set up the web view
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)
        
        # Allow local content to access file URLs and remote URLs
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        # Load the local web page as wallpaper
        logging.info(f"Loading wallpaper from: {self.wallpaper}")
        self.web_view.load(QUrl.fromLocalFile(self.wallpaper.as_posix()))
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Set the window as wallpaper
        WallpaperManager.set_as_wallpaper(int(self.winId()))

        # Load content after main page is finished loading
        self.web_view.loadFinished.connect(self.on_page_load_finished)

        # Open DevTools if in debug mode
        if debug:
            self.open_devtools()

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
        items_dir = Path('addons/').resolve()
        config_file = os.path.join(items_dir, 'config.json')

        config_manager = ConfigManager(config_file)
        hash_manager = HashManager(items_dir)
        injector = Injector(self.web_view)
        updater = Updater(injector, config_manager)
        handler = FileSystemHandler(config_manager, hash_manager, updater.update_items)

        observer = Observer()
        observer.schedule(handler, items_dir, recursive=True)
        observer.start()
        logging.info("File system observer started.")
        
        # Load the initial configuration
        updater.update_items(config_manager.load_config())

    def closeEvent(self, event):
        logging.info("Closing WallpaperLauncher.")
        event.accept()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting application.")
    app = QApplication([])
    wallpaper_app = WallpaperLauncher(debug=True)
    wallpaper_app.show()
    app.exec_()
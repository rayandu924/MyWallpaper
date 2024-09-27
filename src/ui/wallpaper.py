import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from addon.addon_loader import AddonLoader
from addon.addon_watcher import start_addon_watcher
from utils.windows_api import set_as_wallpaper

class WallpaperApp(QMainWindow):
    def __init__(self, web_page_path, debug=False):
        super().__init__()

        # Set up the web view
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Load the local web page as wallpaper
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath(web_page_path)))
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Set the window as a wallpaper while retaining mouse interactions
        set_as_wallpaper(int(self.winId()))

        # Load addons after the main page is loaded
        self.web_view.loadFinished.connect(self.on_page_load_finished)

        # Open DevTools if in debug mode
        if debug:
            self.open_devtools()

    def open_devtools(self):
        # Create a separate window for DevTools
        self.devtools_window = QMainWindow(self)
        dev_tools_view = QWebEngineView(self.devtools_window)

        # Assign DevTools page to the view
        dev_tools_page = QWebEnginePage(self.web_view)
        self.web_view.page().setDevToolsPage(dev_tools_page)
        dev_tools_view.setPage(dev_tools_page)

        self.devtools_window.setCentralWidget(dev_tools_view)
        self.devtools_window.show()

    def on_page_load_finished(self):
        # Directory containing the addons
        addons_dir = os.path.abspath('web/addons')
        addon_loader = AddonLoader(self.web_view)

        # Inject the addons initially
        addon_loader.inject_addons(addons_dir)

        # Start the AddonWatcher to monitor changes
        self.addon_watcher_observer = start_addon_watcher(addon_loader, addons_dir)

    def closeEvent(self, event):
        # Stop the addon watcher when the app is closed
        if hasattr(self, 'addon_watcher_observer'):
            self.addon_watcher_observer.stop()
            self.addon_watcher_observer.join()
        event.accept()

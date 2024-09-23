import os
import ctypes
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from utils import set_as_wallpaper
from addon_manager import AddonLoader  # Import AddonLoader to handle addon injection

class WallpaperApp(QMainWindow):
    def __init__(self, web_page_path, debug=False):
        super().__init__()

        # Create a QWebEngineView to load the web page
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Load the local web page
        self.web_view.load(QUrl.fromLocalFile(web_page_path))

        # Set window flags to make it frameless and full-screen
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Set this PyQt5 window as the wallpaper behind icons
        set_as_wallpaper(int(self.winId()))

        # Load addons after the page has loaded
        self.web_view.loadFinished.connect(self.on_page_load_finished)

        # Open DevTools if debug mode is enabled
        self.devtools_window = None
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
        self.devtools_window.resize(800, 600)

        # Show the DevTools window at start
        self.devtools_window.show()

    def on_page_load_finished(self):
        # Load and inject addons after the main page is fully loaded
        addons_dir = os.path.abspath('web/addons')  # Define the path to the addons folder
        addon_loader = AddonLoader(self.web_view)  # Create an instance of AddonLoader
        addon_loader.inject_addons(addons_dir)  # Inject addons from the addons directory

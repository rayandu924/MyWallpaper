import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl
from addon.addon_loader import AddonLoader
from utils.windows_api import set_as_wallpaper

class WallpaperApp(QMainWindow):
    def __init__(self, web_page_path, debug=False):
        super().__init__()

        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Load the local web page
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath(web_page_path)))
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Set wallpaper
        set_as_wallpaper(int(self.winId()))

        # Load addons after page is loaded
        self.web_view.loadFinished.connect(self.on_page_load_finished)

        if debug:
            self.open_devtools()

    def open_devtools(self):
        from PyQt5.QtWebEngineWidgets import QWebEnginePage
        dev_tools_page = QWebEnginePage(self.web_view)
        self.web_view.page().setDevToolsPage(dev_tools_page)
        dev_tools_view = QWebEngineView()
        dev_tools_view.setPage(dev_tools_page)
        dev_tools_view.show()

    def on_page_load_finished(self):
        addons_dir = os.path.abspath('web/addons')
        addon_loader = AddonLoader(self.web_view)
        addon_loader.inject_addons(addons_dir)

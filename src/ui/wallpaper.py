import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from addon.addon_loader import AddonLoader
from addon.addon_watcher import start_addon_watcher
from utils.windows_api import set_as_wallpaper

class WallpaperApp(QMainWindow):
    def __init__(self, web_path, debug=False):
        super().__init__()
        self.web_path = Path(web_path).resolve()

        # Définir le chemin de la page principale (main/index.html)
        main_page_path = self.web_path / 'main' / 'index.html'

        # Set up the web view
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Charger la page web locale en tant que fond d'écran
        self.web_view.load(QUrl.fromLocalFile(main_page_path.as_posix()))
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Définir la fenêtre comme fond d'écran tout en conservant les interactions souris
        set_as_wallpaper(int(self.winId()))

        # Charger les addons après le chargement de la page principale
        self.web_view.loadFinished.connect(self.on_page_load_finished)

        # Ouvrir DevTools si en mode debug
        if debug:
            self.open_devtools()

    def open_devtools(self):
        """Ouvrir DevTools dans une fenêtre séparée."""
        dev_tools_view = QWebEngineView(self)
        dev_tools_page = QWebEnginePage(self.web_view)
        self.web_view.page().setDevToolsPage(dev_tools_page)
        dev_tools_view.setPage(dev_tools_page)

        # Créer une fenêtre séparée pour DevTools
        self.devtools_window = QMainWindow(self)
        self.devtools_window.setCentralWidget(dev_tools_view)
        self.devtools_window.show()

    def on_page_load_finished(self):
        """Appelée lorsque la page principale est entièrement chargée pour injecter les addons."""
        # Calculer le répertoire des addons relatif à web_path
        addons_dir = self.web_path / 'addons'
        addon_loader = AddonLoader(self.web_view, addons_dir)

        # Injecter les addons initialement
        addon_loader.inject_addons()

        # Démarrer le AddonWatcher pour surveiller les changements dans le répertoire des addons
        self.addon_watcher_observer = start_addon_watcher(addon_loader)

    def closeEvent(self, event):
        """Arrêter l'observateur des addons lorsque l'application est fermée."""
        if hasattr(self, 'addon_watcher_observer'):
            self.addon_watcher_observer.stop()
            self.addon_watcher_observer.join()
        event.accept()
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from addons.addon_loader import AddonLoader
from addons.addon_watcher import start_addon_watcher
from wallpaper.utils.windows_api import set_as_wallpaper


class WallpaperLauncher(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()
        self.wallpaper = Path('src/ui/wallpaper/index.html').resolve()

        # Set up the web view
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Charger la page web locale en tant que fond d'écran
        self.web_view.load(QUrl.fromLocalFile(self.wallpaper.as_posix()))
        self.setWindowFlags(self.windowFlags() | 0x40000)  # FramelessWindowHint
        self.showFullScreen()

        # Importer et définir la fenêtre comme fond d'écran ici pour éviter l'import circulaire
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
        # Calculer le répertoire des addons relatif à wallpaper
        addons_dir = Path('addons/').resolve()

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

def main():
    app = QApplication(sys.argv)
    wallpaper_app = WallpaperLauncher(debug=True)
    wallpaper_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

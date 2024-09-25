import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from PyQt5.QtWidgets import QApplication
from ui.wallpaper import WallpaperApp
from utils.logger import set_logger

def main():
    logger = set_logger('MyWallpaperApp')
    app = QApplication(sys.argv)

    local_file = 'web/index.html'
    wallpaper_app = WallpaperApp(local_file, debug=True)
    wallpaper_app.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

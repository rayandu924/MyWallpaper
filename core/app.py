import sys
import os
from PyQt5.QtWidgets import QApplication
from wallpaper import WallpaperApp
from utils import set_logger

def main():
    # Setup logger
    logger = set_logger('MyWallpaperApp')

    app = QApplication(sys.argv)

    # Path to the local HTML file
    local_file = os.path.abspath('web/index.html')

    # Initialize wallpaper with debug mode enabled
    wallpaper_app = WallpaperApp(local_file, debug=True)
    wallpaper_app.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

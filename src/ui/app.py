import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pathlib import Path
from PyQt5.QtWidgets import QApplication
from ui.wallpaper import WallpaperApp

def main():
    """Main function to start the wallpaper application."""
    app = QApplication(sys.argv)

    web_path = Path('web/').resolve()
    
    wallpaper_app = WallpaperApp(str(web_path), debug=True)
    wallpaper_app.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
import ctypes

class WallpaperManager:
    @staticmethod
    def find_progman():
        user32 = ctypes.windll.user32
        print("Attempting to find Progman window...")
        progman = user32.FindWindowW("Progman", None)
        if not progman:
            print("Progman window not found.")
        else:
            print(f"Progman window found: {progman}")
        return progman

    @staticmethod
    def send_message_to_progman(progman):
        user32 = ctypes.windll.user32
        print("Sending message to Progman to prepare wallpaper...")
        result = user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, None)
        if result == 0:
            print("Failed to send message to Progman.")
        else:
            print("Message sent to Progman successfully.")
        return result

    @staticmethod
    def set_window_as_child(window_id, progman):
        user32 = ctypes.windll.user32
        print(f"Setting window {window_id} as child of Progman...")
        set_parent_result = user32.SetParent(window_id, progman)
        if set_parent_result == 0:
            print("Failed to set window as child of Progman.")
        else:
            print("Window set as child of Progman successfully.")

    @staticmethod
    def set_as_wallpaper(window_id):
        progman = WallpaperManager.find_progman()
        if progman:
            WallpaperManager.send_message_to_progman(progman)
            WallpaperManager.set_window_as_child(window_id, progman)

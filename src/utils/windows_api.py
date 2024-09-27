import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Constants for window styles
GWL_EXSTYLE = -20

# Remove WS_EX_TRANSPARENT to allow mouse interactions
def set_wallpaper_interaction(window_id):
    # Get the current extended window style
    style = user32.GetWindowLongW(window_id, GWL_EXSTYLE)

    # Only apply WS_EX_LAYERED (without WS_EX_TRANSPARENT)
    user32.SetWindowLongW(window_id, GWL_EXSTYLE, style | 0x00080000)  # WS_EX_LAYERED

    # Optionally, set window transparency if needed
    user32.SetLayeredWindowAttributes(window_id, 0, 255, 0x00000002)  # 255 = full opacity

def set_as_wallpaper(window_id):
    progman = user32.FindWindowW("Progman", None)
    result = ctypes.c_void_p()
    user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, ctypes.byref(result))

    def enum_windows_callback(hwnd, lparam):
        shellview = user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
        if shellview != 0:
            global hwnd_workerw
            hwnd_workerw = user32.FindWindowExW(0, hwnd, "WorkerW", None)
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

    if hwnd_workerw:
        user32.ShowWindow(hwnd_workerw, 0)

    # Set the window as a child of Progman
    user32.SetParent(window_id, progman)

    # Ensure mouse interactions
    set_wallpaper_interaction(window_id)

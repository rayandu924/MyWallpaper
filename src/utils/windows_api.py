import ctypes

user32 = ctypes.windll.user32

# Constants for window styles
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

# Remove WS_EX_TRANSPARENT to allow mouse interactions
def set_wallpaper_interaction(window_id):
    # Get the current extended window style
    style = user32.GetWindowLongW(window_id, GWL_EXSTYLE)

    # Remove WS_EX_TRANSPARENT and add WS_EX_LAYERED
    style &= ~WS_EX_TRANSPARENT
    user32.SetWindowLongW(window_id, GWL_EXSTYLE, style | WS_EX_LAYERED)

    # Set window transparency if needed (255 = full opacity)
    user32.SetLayeredWindowAttributes(window_id, 0, 255, 0x00000002)

def set_as_wallpaper(window_id):
    progman = user32.FindWindowW("Progman", None)
    result = ctypes.c_void_p()
    
    # Send message to Progman to prepare it for new wallpaper window
    user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, ctypes.byref(result))

    # Define callback to find the correct WorkerW window
    def enum_windows_callback(hwnd, lparam):
        shellview = user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
        if shellview != 0:
            global hwnd_workerw
            hwnd_workerw = user32.FindWindowExW(0, hwnd, "WorkerW", None)
        return True

    # Enumerate windows to find WorkerW
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

    # Hide the WorkerW window to prevent it from covering our app
    if hwnd_workerw:
        user32.ShowWindow(hwnd_workerw, 0)

    # Set the wallpaper window as a child of Progman
    user32.SetParent(window_id, progman)

    # Ensure mouse interactions
    set_wallpaper_interaction(window_id)

    # Make sure the window captures input events
    user32.SetFocus(window_id)

    # Adjust Z-order to keep the window active but behind desktop icons
    user32.SetWindowPos(window_id, None, 0, 0, 0, 0, 0x0001 | 0x0004)  # SWP_NOMOVE | SWP_NOACTIVATE

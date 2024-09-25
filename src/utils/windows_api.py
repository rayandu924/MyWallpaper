import ctypes

user32 = ctypes.windll.user32

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

    user32.SetParent(window_id, progman)

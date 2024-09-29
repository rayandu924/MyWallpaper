import ctypes

user32 = ctypes.windll.user32

def set_as_wallpaper(window_id):
    progman = user32.FindWindowW("Progman", None)

    # Envoyer un message pour préparer Progman à accepter une nouvelle fenêtre comme fond d'écran
    user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0x0, 1000, None)

    # Trouver et cacher la fenêtre WorkerW
    workerw = ctypes.c_void_p()
    def enum_windows_callback(hwnd, lparam):
        shellview = user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
        if shellview != 0:
            nonlocal workerw
            workerw = user32.FindWindowExW(0, hwnd, "WorkerW", None)
        return True

    # Enumérer les fenêtres pour trouver WorkerW
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

    # Cacher la fenêtre WorkerW si elle est trouvée
    if workerw:
        user32.ShowWindow(workerw, 0)

    # Définir la fenêtre comme enfant de Progman
    user32.SetParent(window_id, progman)

import sys, os
import webview
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from addons.addon_manager_api import AddonManagerAPI

def main():
    api = AddonManagerAPI(addons_dir='addons')

    # Démarrer l'interface PyWebView avec l'API
    window = webview.create_window('Addon Manager', '../../ui/addons_manager/index.html', js_api=api)
    webview.start(debug=True)  # Active le mode debug
    
if __name__ == '__main__':
    main()

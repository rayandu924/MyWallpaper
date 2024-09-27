import webview
import os
import json
import logging

# Configurer le logging pour afficher des informations détaillées
logging.basicConfig(level=logging.INFO)

ADDONS_DIR = './web/addons'

def get_addons_list():
    """Retourne la liste des dossiers d'addons"""
    logging.info(f"Recherche des addons dans le dossier : {ADDONS_DIR}")
    addons = [d for d in os.listdir(ADDONS_DIR) if os.path.isdir(os.path.join(ADDONS_DIR, d))]
    logging.info(f"Addons trouvés : {addons}")
    return addons

def get_config(addon):
    """Retourne la configuration d'un addon à partir de l'index.html"""
    config_path = os.path.join(ADDONS_DIR, addon, 'index.html')
    logging.info(f"Chargement de la configuration pour l'addon : {addon} depuis {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
            end = content.find('</script>', start)
            json_str = content[start:end]
            logging.info(f"Configuration chargée : {json_str}")
            return json.loads(json_str)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture de la configuration pour l'addon {addon}: {e}")
        return None

def save_config(addon, config):
    """Sauvegarde la configuration mise à jour dans l'index.html"""
    config_path = os.path.join(ADDONS_DIR, addon, 'index.html')
    logging.info(f"Sauvegarde de la nouvelle configuration pour l'addon : {addon} dans {config_path}")
    
    try:
        with open(config_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            start = content.find('<script id="config" type="application/json">') + len('<script id="config" type="application/json">')
            end = content.find('</script>', start)
            
            new_content = content[:start] + json.dumps(config, indent=4) + content[end:]
            f.seek(0)
            f.write(new_content)
            f.truncate()
            logging.info(f"Configuration sauvegardée avec succès pour l'addon : {addon}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde de la configuration pour l'addon {addon}: {e}")

def pywebview_api():
    """Fonctions disponibles pour interagir avec le frontend PyWebView"""
    class Api:
        def get_addons(self):
            logging.info("Récupération de la liste des addons via l'API PyWebView")
            return get_addons_list()

        def load_config(self, addon):
            logging.info(f"Chargement de la configuration de l'addon {addon} via l'API PyWebView")
            return get_config(addon)

        def save_config(self, addon, config):
            logging.info(f"Sauvegarde de la configuration de l'addon {addon} via l'API PyWebView")
            save_config(addon, config)
            return {"status": "Config saved"}

    return Api()

# Initialisation de PyWebView
if __name__ == '__main__':
    api = pywebview_api()
    window = webview.create_window('Addon Manager', 'index.html', js_api=api)
    webview.start(debug=True)  # Active le mode debug


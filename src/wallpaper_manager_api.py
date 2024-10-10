import logging
import os
from flask import Flask, jsonify, request, send_from_directory
from src.json_manager import JsonManager
from src.file_manager import FileManager
from pathlib import Path
from src.html_manager import HtmlManager
from src.item_manager import ItemManager

flask_app = Flask(__name__, static_folder='static')

@flask_app.route("/update_item", methods=['POST'])
def update_item():
    data = request.get_json()
    logging.info(f"Received data to modify page: {data}")
    if wallpaper_app:
        # Exécuter du JavaScript pour modifier l'élément de la page
        wallpaper_app.web_view.page().runJavaScript(f"document.body.style.backgroundColor = '{data['color']}'")
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Wallpaper app not initialized"}), 500

@flask_app.route("/get_config", methods=['GET'])
def get_config():
    items_dir = Path('items/').resolve()
    config_file = os.path.join(items_dir, 'config.json')
    config_data = JsonManager.load_json(config_file)
    return jsonify(config_data)

@flask_app.route("/save_item_config/<item_name>", methods=['POST'])
def save_item_config(item_name):
    try:
        # Récupérer la nouvelle configuration envoyée par le client
        new_config = request.get_json()

        if not isinstance(new_config, dict):
            raise ValueError(f"Invalid config format for item '{item_name}'")

        # Chemin vers le fichier HTML de l'item
        item_dir = Path('items', item_name).resolve()
        index_file = os.path.join(item_dir, 'index.html')

        # Lire le contenu HTML actuel
        html_content = FileManager.read_file(index_file)
        if html_content is None:
            raise FileNotFoundError(f"index.html not found for item '{item_name}'")

        # Convertir la configuration en JSON string formaté
        new_config_json = JsonManager.to_string(new_config)

        # Mettre à jour l'élément <script id="config"> avec la nouvelle configuration
        updated_html = HtmlManager.update_element_by_id(html_content, 'config', new_config_json)
        if updated_html is None:
            raise ValueError(f"Failed to update config for item '{item_name}'")

        # Sauvegarder le fichier HTML mis à jour
        FileManager.write_file(index_file, updated_html)
        items_dir = Path('items/').resolve()
        config_file = os.path.join(items_dir, 'config.json')
        config_data = JsonManager.load_json(config_file)
        tmp = next((item for item in config_data.get('items', []) if item.get('name') == item_name), None)
        print(tmp)
        ItemManager.update_item(wallpaper_app.web_view, tmp)

        return jsonify({"success": True, "message": f"Configuration saved for item '{item_name}'"})

    except FileNotFoundError as e:
        logging.error(e)
        return jsonify({"success": False, "message": str(e)}), 404
    except ValueError as e:
        logging.error(e)
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@flask_app.route("/get_item_config/<item_name>", methods=['GET'])
def get_item_config(item_name):
    item_dir = Path('items', item_name).resolve()
    index_file = os.path.join(item_dir, 'index.html')
    html_content = FileManager.read_file(index_file)
    config_script = HtmlManager.get_element_by_id(html_content, 'config')
    config_json = config_script.get_text().strip()
    config_data = JsonManager.parse_json(config_json)
    return jsonify(config_data)

# Servir les fichiers HTML statiques depuis le répertoire 'static'
@flask_app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(flask_app.static_folder, path)

def start_api(wallpaper_app_instance):
    global wallpaper_app
    wallpaper_app = wallpaper_app_instance
    flask_app.run(port=5000, use_reloader=False)

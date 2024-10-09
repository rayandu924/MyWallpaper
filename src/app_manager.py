import webview
import logging
import os
from pathlib import Path
from src.json_manager import JsonManager
from src.file_manager import FileManager
from src.html_manager import HtmlManager

class AppManager:
    @staticmethod
    def create_app():
        api = Api()
        window = webview.create_window(
            'Addon Manager',
            'ui/addons_manager/index.html',
            js_api=api,
            width=1200,
            height=800,
            resizable=True,
        )
        webview.start(debug=True)


class Api: 
    def get_config(self):                
        items_dir = Path('items/').resolve()
        config_file = os.path.join(items_dir, 'config.json')
             
        return JsonManager.load_json(config_file)

    def get_item_config(self, item_name):
        # Chemin vers le fichier index.html pour cet item
        item_dir = Path('items', item_name).resolve()
        index_file = os.path.join(item_dir, 'index.html')

        # Utilisation de FileManager pour lire le contenu du fichier HTML
        html_content = FileManager.read_file(index_file)
        config_script = HtmlManager.get_element_by_id(html_content, 'config')
        config_json = config_script.string.strip()
        config_data = JsonManager.parse_json(config_json)
        return config_data
    
    def save_item_config(self, item_name, new_config):
        # Chemin vers le fichier index.html pour cet item
        item_dir = Path('items', item_name).resolve()
        index_file = os.path.join(item_dir, 'index.html')

        # Charger le fichier HTML actuel
        html_content = FileManager.read_file(index_file)

        if html_content is None:
            raise FileNotFoundError(f"index.html not found for item '{item_name}'")

        # Convertir la nouvelle configuration en JSON string formaté
        new_config_json = JsonManager.to_string(new_config)

        # Mettre à jour le contenu de l'élément <script id="config">
        updated_html = HtmlManager.update_element_by_id(html_content, 'config', new_config_json)

        if updated_html is None:
            raise ValueError(f"Failed to update config in {index_file}")

        # Sauvegarder le fichier HTML mis à jour
        FileManager.write_file(index_file, updated_html)

        logging.info(f"Configuration updated successfully for item '{item_name}'")
        
        return {
            "success": True,
            "message": f"Configuration updated successfully for item '{item_name}'"
        }
    
if __name__ == '__main__':
    AppManager.create_app()

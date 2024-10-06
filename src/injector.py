import logging
from PyQt5.QtCore import QUrl

class Injector:
    def __init__(self, view):
        self.view = view
        logging.info("Injector initialized.")

    def inject_content(self, item_name, item_path, position=None):
        logging.info(f"Injecting content for item: {item_name}, path: {item_path}, position: {position}")
        script = f"""
        console.log('Attempting to inject item: {item_name}');
        var existingElement = document.querySelector('[item="{item_name}"]');
        var position = {position if position is not None else 'null'};

        if (existingElement) {{
            console.log('Removing existing element for item: {item_name}');
            existingElement.remove();
        }}

        var element = document.createElement('iframe');
        element.setAttribute('item', '{item_name}');
        element.src = '{QUrl.fromLocalFile(item_path).toString()}';

        if (position !== null && position >= 0 && position < document.body.children.length) {{
            console.log('Inserting iframe at position:', position);
            document.body.insertBefore(element, document.body.children[position]);
        }} else {{
            console.log('Appending iframe to the document body');
            document.body.appendChild(element);
        }}
        """
        self.view.page().runJavaScript(script)

    def remove_content(self, item_name):
        logging.info(f"Removing content for item: {item_name}")
        script = f"""
        var element = document.querySelector('[item="{item_name}"]');
        if (element) {{
            element.remove();
        }}
        """
        self.view.page().runJavaScript(script)

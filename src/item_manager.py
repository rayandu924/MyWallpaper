import logging
from PyQt5.QtCore import QUrl

class ItemManager:

    @staticmethod
    def update_items(view, items):
        logging.info("Updating items")
        for item in items:
            ItemManager.update_item(view, item)
    
    @staticmethod
    def update_item(view, item):
        logging.info(f"Updating item: {item['name']}")
        if item.get("enabled"):
            ItemManager.inject_item(view, item)
        else:
            ItemManager.remove_item(view, item)

    @staticmethod
    def inject_item(view, item):
        logging.info(f"Injecting item: {item['name']}")
        script = f"""
        console.log('Attempting to inject item: {item['name']}');
        var existingElement = document.querySelector('[item="{item['name']}"]');
        var position = {item['position']};

        if (existingElement) {{
            console.log('Removing existing element for item: {item['name']}');
            existingElement.remove();
        }}

        var element = document.createElement('iframe');
        element.setAttribute('item', '{item['name']}');
        element.src = '{item['path']}';

        // Set z-index to ensure proper stacking order
        element.style.zIndex = '{item['position']}';

        if (position !== null && position >= 0 && position < document.body.children.length) {{
            console.log('Inserting iframe at position:', position);
            document.body.insertBefore(element, document.body.children[position]);
        }} else {{
            console.log('Appending iframe to the document body');
            document.body.appendChild(element);
        }}
        """
        view.page().runJavaScript(script)

    @staticmethod
    def remove_item(view, item):
        logging.info(f"Removing item: {item['name']}")
        script = f"""
        var element = document.querySelector('[item="{item['name']}"]');
        if (element) {{
            element.remove();
        }}
        """
        view.page().runJavaScript(script)

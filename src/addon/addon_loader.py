import os
from PyQt5.QtCore import QUrl
from bs4 import BeautifulSoup

class AddonLoader:
    def __init__(self, web_view):
        self.web_view = web_view

    def inject_addons(self, addons_dir):
        """Inject all addons from the addons directory into the web view."""
        if not os.path.exists(addons_dir):
            print(f"Addons directory does not exist: {addons_dir}")
            return

        addons = self.get_addon_files(addons_dir)
        for addon_name, addon_path in addons:
            self.inject_html_content(addon_name, addon_path)

    def get_addon_files(self, addons_dir):
        """Return a list of (addon_name, addon_path) from the addons directory."""
        addons = []
        for addon_name in os.listdir(addons_dir):
            addon_path = os.path.join(addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                addons.append((addon_name, addon_path))
        return addons

    def inject_html_content(self, addon_name, addon_path):
        """Inject an iframe for each addon into the web view."""
        # Créer une iframe pour charger l'addon
        iframe_script = f"""
        var existingIframe = document.querySelector('iframe[addon="{addon_name}"]');
        if (existingIframe) {{
            existingIframe.remove();
        }}
        
        var newIframe = document.createElement('iframe');
        newIframe.setAttribute('addon', '{addon_name}');
        newIframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';
        newIframe.style.width = '100%';
        newIframe.style.height = '100%';
        newIframe.style.border = 'none';
        document.body.appendChild(newIframe);
        """

        # Injecter et exécuter le script dans le WebView
        self.web_view.page().runJavaScript(iframe_script)

import os
from PyQt5.QtCore import QUrl

class AddonLoader:
    def __init__(self, web_view, addons_dir):
        self.web_view = web_view
        self.addons_dir = addons_dir

    def inject_addons(self):
        """Inject all valid addons into the web view."""
        if not os.path.exists(self.addons_dir):
            print(f"Addons directory does not exist: {self.addons_dir}")
            return

        for addon_name in os.listdir(self.addons_dir):
            addon_path = os.path.join(self.addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                self.inject_html_content(addon_name, addon_path)

    def inject_html_content(self, addon_name, addon_path):
        """Inject an iframe for the addon."""
        script = f"""
        var iframe = document.querySelector('iframe[addon="{addon_name}"]');
        if (iframe) iframe.remove();

        iframe = document.createElement('iframe');
        iframe.setAttribute('addon', '{addon_name}');
        iframe.src = '{QUrl.fromLocalFile(addon_path).toString()}';
        document.body.appendChild(iframe);
        """
        self.web_view.page().runJavaScript(script)

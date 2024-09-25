import os
from PyQt5.QtCore import QUrl

class AddonLoader:
    def __init__(self, web_view):
        self.web_view = web_view

    def inject_addons(self, addons_dir):
        """Inject all addons from the addons directory into the web view."""
        if not os.path.exists(addons_dir):
            print(f"Addons directory does not exist: {addons_dir}")
            return

        addons = self.get_addon_files(addons_dir)
        for addon_name, addon_url in addons:
            self.inject_iframe(addon_name, addon_url)

    def get_addon_files(self, addons_dir):
        """Return a list of (addon_name, addon_url) tuples from the addons directory."""
        addons = []
        for addon_name in os.listdir(addons_dir):
            addon_path = os.path.join(addons_dir, addon_name, "index.html")
            if os.path.exists(addon_path):
                addon_url = QUrl.fromLocalFile(os.path.abspath(addon_path))
                addons.append((addon_name, addon_url))
        return addons

    def inject_iframe(self, addon_name, addon_url):
        """Inject or update an iframe in the web view."""
        script = f"""
        var iframe = document.getElementById("{addon_name}_iframe");
        if (iframe) {{
            iframe.src = "{addon_url.toString()}";
        }} else {{
            iframe = document.createElement('iframe');
            iframe.id = "{addon_name}_iframe";
            iframe.src = "{addon_url.toString()}";
            iframe.style.position = "absolute";
            iframe.style.top = "0";
            iframe.style.left = "0";
            iframe.style.width = "100vw";
            iframe.style.height = "100vh";
            iframe.style.border = "none";
            document.body.appendChild(iframe);
        }}
        """
        self.web_view.page().runJavaScript(script)

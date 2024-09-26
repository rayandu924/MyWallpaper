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
        """Inject the body content, CSS, and JS from the addon's index.html."""
        with open(addon_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML file with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Step 1: Remove existing content, CSS, and JS before re-injecting
        removal_script = f"""
        // Remove existing addon HTML content
        var existing_addon = document.getElementById("{addon_name}_content");
        if (existing_addon) {{
            console.log("Removing existing addon content: {addon_name}");
            existing_addon.remove();
        }}

        // Remove associated CSS
        var css_links = document.querySelectorAll('link[addon="{addon_name}"]');
        css_links.forEach(link => link.remove());

        // Remove associated JS
        var js_scripts = document.querySelectorAll('script[addon="{addon_name}"]');
        js_scripts.forEach(script => script.remove());
        """
        self.web_view.page().runJavaScript(removal_script)

        # Step 2: Inject the new content
        inject_script = f"""
        var addon_body = document.createElement('div');
        addon_body.id = "{addon_name}_content";
        addon_body.innerHTML = `{soup.body.decode_contents()}`;
        document.body.appendChild(addon_body);
        """
        self.web_view.page().runJavaScript(inject_script)

        # Step 3: Inject CSS and JS after ensuring the old content is removed and new content is injected
        self.inject_css(soup, addon_path, addon_name)
        self.inject_js(soup, addon_path, addon_name)

    def inject_css(self, soup, addon_path, addon_name):
        """Inject CSS into the head of the web view."""
        base_dir = os.path.dirname(addon_path)

        # Inject <link> (CSS)
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = self.resolve_url(href, base_dir)
                script = f"""
                var link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = "{css_url}";
                link.setAttribute('addon', "{addon_name}");  // Mark with addon name for later removal
                document.head.appendChild(link);
                """
                self.web_view.page().runJavaScript(script)

    def inject_js(self, soup, addon_path, addon_name):
        """Inject external JS and inline scripts into the head of the web view."""
        base_dir = os.path.dirname(addon_path)

        # Inject external <script> (JavaScript) tags
        for script_tag in soup.find_all('script', src=True):
            src = script_tag.get('src')
            if src:
                js_url = self.resolve_url(src, base_dir)
                script = f"""
                var script = document.createElement('script');
                script.src = "{js_url}";
                script.setAttribute('addon', "{addon_name}");  // Mark with addon name for later removal
                document.head.appendChild(script);
                """
                self.web_view.page().runJavaScript(script)

        # Inject inline <script> (JavaScript) tags
        for script_tag in soup.find_all('script', src=False):
            inline_script = script_tag.string or ""
            if inline_script.strip():  # Avoid empty scripts
                script = f"""
                var script = document.createElement('script');
                script.innerHTML = `{inline_script}`;
                script.setAttribute('addon', "{addon_name}");  // Mark with addon name for later removal
                document.head.appendChild(script);
                """
                self.web_view.page().runJavaScript(script)

    def resolve_url(self, url, base_dir):
        """Resolve the URL, handling both local relative paths and remote URLs."""
        if url.startswith(('http://', 'https://')):
            return url  # Already an absolute URL, return it as is
        else:
            # If it's a local file, resolve the relative path
            local_path = os.path.join(base_dir, url)
            if os.path.exists(local_path):
                return QUrl.fromLocalFile(os.path.abspath(local_path)).toString()
            else:
                print(f"Warning: File does not exist - {local_path}")
                return ''  # Return empty string if file doesn't exist

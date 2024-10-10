import logging
from bs4 import BeautifulSoup

class HtmlManager:
    @staticmethod
    def get_element_by_id(html_content, element_id):
        try:
            # Parse le contenu HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            element = soup.find(id=element_id)

            if element:
                return element
            else:
                # Lever une exception si l'élément n'est pas trouvé
                raise ValueError(f"Element with id='{element_id}' not found in HTML content.")
        except Exception as e:
            raise ValueError(f"Error getting element with id='{element_id}': {e}")

    @staticmethod
    def update_element_by_id(html_content, element_id, new_content):
        try:
            # Parse le contenu HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            element = soup.find(id=element_id)

            if element:
                # Met à jour le contenu de l'élément
                element.string = new_content
                logging.info(f"Element with id='{element_id}' updated successfully.")
                return str(soup)  # Retourne le HTML modifié sous forme de chaîne
            else:
                # Lever une exception si l'élément n'est pas trouvé
                raise ValueError(f"Element with id='{element_id}' not found.")
        except Exception as e:
            raise ValueError(f"Error updating element with id='{element_id}': {e}")

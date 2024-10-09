import logging
from bs4 import BeautifulSoup
from src.file_manager import FileManager

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
                logging.error(f"Error: Element with id='{element_id}' not found in HTML content.")
                return None
        except Exception as e:
            logging.error(f"Error parsing HTML: {e}")
            return None

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
                logging.error(f"Error: Element with id='{element_id}' not found.")
                return None
        except Exception as e:
            logging.error(f"Error updating element in HTML: {e}")
            return None
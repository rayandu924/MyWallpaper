import requests

url = 'http://127.0.0.1:5000/modify_page'
data = {
    'color': '#FF0000'  # Remplace par la couleur que tu souhaites
}

response = requests.post(url, json=data)

print(response.json())  # Affiche la réponse de l'API

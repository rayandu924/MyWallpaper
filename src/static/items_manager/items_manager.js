import { call_api } from './api_manager.js';
import { create_element } from './elements_manager.js'; // On utilise create_element
import { create_input } from './inputs_manager.js'; // On utilise create_input

// Fonction pour créer un élément de la liste
function create_item(item) {
    // Utilise create_element pour créer un élément de la liste
    const li = create_element({
        elementType: 'li',
        attributes: {
            'data-name': item.name, // Ajoute l'attribut data-name pour identifier l'item
            class: 'item-item' // Ajoute la classe à l'item
        },
        events: {
            click: async () => {
                console.log('item sélectionné:', item.name);

                // Appel API pour obtenir la configuration spécifique de l'item
                let item_config = await call_api(`http://localhost:5000/get_item_config/${item.name}`);

                // Gestion des erreurs possibles
                if (item_config.success === false) {
                    console.error('Erreur lors du chargement de la configuration:', item_config.message);
                    return;
                }

                // Met à jour la liste des configurations
                const config_list = document.getElementById('item-config');
                config_list.innerHTML = ''; // Efface la configuration précédente

                // Crée des inputs basés sur la configuration de l'item
                let inputs = create_item_config(item.name, item_config);

                // Ajoute chaque input à la liste des configurations
                inputs.forEach(input => config_list.appendChild(input));
            }
        },
        children: [item.name] // Ajoute le nom de l'item comme contenu textuel
    });

    return li; // Retourne l'élément <li> créé
}

// Fonction pour créer les inputs avec les labels pour chaque clé de config
function create_item_config(item_name, config) {
    const elements = [];

    for (let key in config) {
        // Créer le label pour la clé
        const label = create_element({
            elementType: 'label',
            children: [key], // Le texte du label sera la clé de la config
            attributes: {
                for: key // Associe le label à l'input (si nécessaire)
            }
        });

        // Créer l'input correspondant à la valeur de la clé
        const input = create_input(config[key], async (event) => {
            // Met à jour la configuration avec la nouvelle valeur
            config[key].value = event.target.value;

            // Appel API pour sauvegarder la nouvelle configuration
            let response = await call_api(`http://localhost:5000/save_item_config/${item_name}`, 'POST', config);

            // Gestion des erreurs lors de la sauvegarde
            if (response.success === false) {
                console.error('Erreur lors de la sauvegarde de la configuration:', response.message);
                return;
            }

            console.log('Configuration sauvegardée avec succès pour l\'item:', item_name);
        });

        // Créer un conteneur pour regrouper le label et l'input
        const container = create_element({
            elementType: 'div',
            children: [label, input], // On regroupe le label et l'input
            attributes: {
                class: 'config-item' // Ajoute une classe pour pouvoir styliser chaque config si besoin
            }
        });

        elements.push(container); // Ajoute le conteneur dans la liste des éléments
    }

    return elements; // Retourne la liste des conteneurs (label + input)
}

// Fonction pour créer et retourner les éléments des items sans les ajouter au DOM
export function create_items(items) {
    const elements = [];
    console.log('items:', items);
    // Parcourt chaque item et sa configuration correspondante pour créer les éléments
    items.forEach((item) => {
        const li = create_item(item); // Crée l'élément <li> pour chaque item
        elements.push(li); // Ajoute l'élément créé dans le tableau
    });

    return elements; // Renvoie la liste des éléments
}

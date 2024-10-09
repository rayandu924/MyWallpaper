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
                
                // Charger depuis l'API la configuration de l'item
                let item_config = await window.pywebview.api.get_item_config(item.name);

                const config_list = document.getElementById('item-config');
                config_list.innerHTML = ''; // Efface la configuration précédente

                let inputs = create_item_config(item.name, item_config);

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
            console.log(`Sauvegarde de la valeur pour ${key}:`, event.target.value);
            config[key].value = event.target.value;
            await window.pywebview.api.save_item_config(item_name, config);            
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

import { call_api } from './api_manager.js';
import { create_items } from './items_manager.js';

document.addEventListener('DOMContentLoaded', function () {
    main();
});

async function main() {
    const items_list = document.getElementById('items');
    items_list.innerHTML = ''; // Effacer la liste précédente

    const config = await call_api('http://localhost:5000/get_config');
    const elements = create_items(config.items);
    elements.forEach(element => items_list.appendChild(element));
}

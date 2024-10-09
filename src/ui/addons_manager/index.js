import { create_items } from './items_manager.js';

document.addEventListener('DOMContentLoaded', function () {
    checkPyWebViewReady();
});

function checkPyWebViewReady() {
    if (window.pywebview && window.pywebview.api) {
        main();
    } else {
        setTimeout(checkPyWebViewReady, 100);
    }
}

async function main() {
    const items_list = document.getElementById('items');
    items_list.innerHTML = ''; // Effacer la liste précédente
    let config = await window.pywebview.api.get_config();
    const elements = create_items(config.items);
    elements.forEach(element => items_list.appendChild(element));
}

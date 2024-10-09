import { create_element } from './elements_manager.js';

export function create_input(item_config, onInputCallback) {
    const { elementType = 'input', type } = item_config;
    const element = create_element({
        elementType: elementType,
        attributes: { ...item_config },
        events: {
            input: (event) => {
                if (elementType === 'input' && (type === 'checkbox' || type === 'radio')) {
                    item_config.checked = event.target.checked;
                    item_config.value = event.target.checked;
                } else if (elementType === 'input' && type === 'file') {
                    item_config.files = event.target.files;
                } else {
                    item_config.value = event.target.value;
                }
                if (onInputCallback) onInputCallback(event);
            },
            change: (event) => {
                if (elementType === 'input' && (type === 'checkbox' || type === 'radio')) {
                    item_config.checked = event.target.checked;
                    item_config.value = event.target.checked;
                } else if (elementType === 'input' && type === 'file') {
                    item_config.files = event.target.files;
                } else {
                    item_config.value = event.target.value;
                }
                if (onInputCallback) onInputCallback(event);
            }
        },
        styles: item_config.styles || {}
    });
    return element;
}

/*
// Sélection de la div "test"
const testDiv = document.getElementById('test');

// Liste pour stocker tous les éléments créés
const createdElements = [];

// 1. Sélecteur de couleur (Color Picker)
const colorPickerConfig = {
    elementType: 'input',
    type: 'color',
    value: '#ff0000' // couleur par défaut rouge
};

const colorPicker = create_input(colorPickerConfig, (event) => {
    console.log('Couleur sélectionnée:', colorPickerConfig.value);
});

createdElements.push(document.createTextNode('Sélecteur de couleur : '));
createdElements.push(colorPicker);
createdElements.push(document.createElement('br'));

// 2. Slider (Input de type range)
const sliderConfig = {
    type: 'range',
    min: 0,
    max: 100,
    value: 50,
    step: 1,
};

const sliderValueDisplay = document.createElement('span');
sliderValueDisplay.textContent = sliderConfig.value;

const sliderInput = create_input(sliderConfig, (event) => {
    sliderValueDisplay.textContent = sliderConfig.value;
    console.log('Valeur du slider:', sliderConfig.value);
});

createdElements.push(document.createTextNode('Slider : '));
createdElements.push(sliderInput);
createdElements.push(sliderValueDisplay);
createdElements.push(document.createElement('br'));

// 3. Case à cocher (Checkbox)
const checkboxConfig = {
    elementType: 'input',
    type: 'checkbox',
    checked: true
};

const checkboxLabel = document.createElement('label');
checkboxLabel.textContent = 'Activer l\'option';
const checkboxInput = create_input(checkboxConfig, (event) => {
    console.log('Checkbox cochée:', checkboxConfig.checked);
});
checkboxLabel.insertBefore(checkboxInput, checkboxLabel.firstChild);

createdElements.push(checkboxLabel);
createdElements.push(document.createElement('br'));

// 4. Boutons radio (Radio Buttons)
const radioOptions = [
    { value: 'option1', label: 'Option 1', checked: true },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' }
];

createdElements.push(document.createTextNode('Boutons radio : '));
createdElements.push(document.createElement('br'));

radioOptions.forEach(option => {
    const radioConfig = {
        elementType: 'input',
        type: 'radio',
        name: 'radioGroup',
        value: option.value,
        checked: option.checked || false
    };

    const radioInput = create_input(radioConfig, (event) => {
        console.log('Option sélectionnée:', event.target.value);
    });

    const label = document.createElement('label');
    label.textContent = option.label;
    label.insertBefore(radioInput, label.firstChild);

    createdElements.push(label);
    createdElements.push(document.createElement('br'));
});

// 5. Sélecteur de date (Date Picker)
const datePickerConfig = {
    elementType: 'input',
    type: 'date',
    value: '2023-10-10'
};

const datePicker = create_input(datePickerConfig, (event) => {
    console.log('Date sélectionnée:', datePickerConfig.value);
});

createdElements.push(document.createTextNode('Sélecteur de date : '));
createdElements.push(datePicker);
createdElements.push(document.createElement('br'));

// 6. Input de temps (Time Picker)
const timePickerConfig = {
    elementType: 'input',
    type: 'time',
    value: '12:30'
};

const timePicker = create_input(timePickerConfig, (event) => {
    console.log('Heure sélectionnée:', timePickerConfig.value);
});

createdElements.push(document.createTextNode('Sélecteur de temps : '));
createdElements.push(timePicker);
createdElements.push(document.createElement('br'));

// 7. Input de fichier (File Input)
const fileInputConfig = {
    elementType: 'input',
    type: 'file',
    accept: 'image/*',
    multiple: true
};

const fileInput = create_input(fileInputConfig, (event) => {
    console.log('Fichiers sélectionnés:', event.target.files);
});

createdElements.push(document.createTextNode('Sélecteur de fichier : '));
createdElements.push(fileInput);
createdElements.push(document.createElement('br'));

// 8. Textarea
const textareaConfig = {
    elementType: 'textarea',
    value: 'Texte initial',
    rows: 4,
    cols: 50,
    placeholder: 'Entrez votre message ici...'
};

const textarea = create_input(textareaConfig, (event) => {
    console.log('Contenu de la textarea:', textareaConfig.value);
});

createdElements.push(document.createTextNode('Zone de texte : '));
createdElements.push(document.createElement('br'));
createdElements.push(textarea);
createdElements.push(document.createElement('br'));

// 9. Select (Menu déroulant)
const selectConfig = {
    elementType: 'select',
    options: [
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2', selected: true },
        { value: 'option3', label: 'Option 3' }
    ]
};

const selectElement = create_input(selectConfig, (event) => {
    console.log('Option sélectionnée:', selectElement.value);
});

createdElements.push(document.createTextNode('Menu déroulant : '));
createdElements.push(selectElement);
createdElements.push(document.createElement('br'));

// Injection de tous les éléments dans la div "test"
createdElements.forEach(element => {
    testDiv.appendChild(element);
});*/
// Generalized function for creating any HTML element
export function create_element({ elementType, attributes = {}, events = {}, styles = {}, children = [] }) {
    const element = document.createElement(elementType);

    // Set attributes
    for (const [attrName, attrValue] of Object.entries(attributes)) {
        if (!['styles', 'events', 'children'].includes(attrName)) {
            if (attrName === 'value') {
                if (['input', 'textarea', 'select'].includes(elementType)) {
                    element.value = attrValue;
                } else {
                    element.textContent = attrValue;
                }
            } else if (attrName === 'checked') {
                element.checked = attrValue;
            } else {
                element.setAttribute(attrName, attrValue);
            }
        }
    }

    // Handle specific cases for select elements
    if (elementType === 'select' && attributes.options) {
        attributes.options.forEach(optionConfig => {
            const option = document.createElement('option');
            option.value = optionConfig.value;
            option.textContent = optionConfig.label || optionConfig.value;
            if (optionConfig.selected) option.selected = true;
            element.appendChild(option);
        });
    }

    // Add event listeners
    for (const [eventName, eventHandler] of Object.entries(events)) {
        element.addEventListener(eventName, eventHandler);
    }

    // Apply styles
    Object.assign(element.style, styles);

    // Append child elements if provided
    children.forEach(child => {
        if (typeof child === 'string') {
            element.innerHTML += child; // Add plain text or HTML
        } else {
            element.appendChild(child); // Add DOM elements
        }
    });

    return element;
}

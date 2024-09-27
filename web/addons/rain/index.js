// Fonction pour charger la configuration à partir du script JSON dans le HTML
function loadConfigFromHtml() {
    const configScript = document.getElementById('config');
    return JSON.parse(configScript.textContent);
}

function initRainEffect(config) {
    const rainContainer = document.getElementById('rain-container');
    
    const createDrop = () => {
        const drop = document.createElement('div');
        drop.className = 'rain-drop';
        
        const size = getRandom(config.dropSizeMin.value, config.dropSizeMax.value);
        const length = getRandom(config.dropLengthMin.value, config.dropLengthMax.value);
        const speed = getRandom(config.dropSpeedMin.value, config.dropSpeedMax.value);
        const startX = Math.random() * 100;
        
        drop.style.setProperty('--drop-size', `${size}px`);
        drop.style.setProperty('--drop-length', `${length}px`);
        drop.style.setProperty('--drop-speed', `${speed}s`);
        drop.style.setProperty('--drop-color', config.dropColor.value);
        drop.style.setProperty('--drop-angle', `${config.dropAngle.value}deg`);
        drop.style.left = `${startX}%`;

        rainContainer.appendChild(drop);
        
        setTimeout(() => {
            rainContainer.removeChild(drop);
        }, speed * 1000);
    };

    setInterval(createDrop, config.dropFrequency.value);
}

function getRandom(min, max) {
    return Math.random() * (max - min) + min;
}

// Charger la configuration depuis le HTML et initialiser l'effet pluie
const config = loadConfigFromHtml();
initRainEffect(config);

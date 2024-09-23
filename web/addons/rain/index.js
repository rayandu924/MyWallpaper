document.addEventListener('DOMContentLoaded', function() {
    const config = {
        dropSizeMin: 2,
        dropSizeMax: 4,
        dropLengthMin: 10,
        dropLengthMax: 20,
        dropFrequency: 5,  // in milliseconds
        dropSpeedMin: 2,     // in seconds
        dropSpeedMax: 1.5,     // in seconds
        dropColor: "#fc03c6",
        dropAngle: 15 // degrees
    };

    function initRainEffect() {
        const rainContainer = document.getElementById('rain-container');
        const createDrop = () => {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            
            // Randomize drop properties
            const size = getRandom(config.dropSizeMin, config.dropSizeMax);
            const length = getRandom(config.dropLengthMin, config.dropLengthMax);
            const speed = getRandom(config.dropSpeedMin, config.dropSpeedMax);
            const startX = Math.random() * 100;
            
            drop.style.setProperty('--drop-size', `${size}px`);
            drop.style.setProperty('--drop-length', `${length}px`);
            drop.style.setProperty('--drop-speed', `${speed}s`);
            drop.style.setProperty('--drop-color', config.dropColor);
            drop.style.setProperty('--drop-angle', `${config.dropAngle}deg`);
            
            drop.style.left = `${startX}%`;

            rainContainer.appendChild(drop);
            
            // Remove the drop after animation is done
            setTimeout(() => {
                rainContainer.removeChild(drop);
            }, speed * 1000);
        };

        // Generate drops at the specified frequency
        setInterval(createDrop, config.dropFrequency);
    }

    function getRandom(min, max) {
        return Math.random() * (max - min) + min;
    }

    initRainEffect();
});

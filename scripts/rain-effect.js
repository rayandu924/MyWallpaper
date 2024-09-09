var makeItRain = function() {
    // Clear out everything
    var rainContainer = document.querySelector('.rain');
    rainContainer.innerHTML = '';

    var drops = '';
    var totalDrops = 100; // Nombre total de gouttes

    for (var i = 0; i < totalDrops; i++) {
        var leftPosition = Math.random() * 100; // Position horizontale aléatoire
        var animationDelay = Math.random(); // Délai d'animation aléatoire
        var animationDuration = 0.5 + Math.random(); // Durée d'animation aléatoire

        drops += `
            <div class="drop" 
                style="left: ${leftPosition}%; 
                       animation-delay: ${animationDelay}s; 
                       animation-duration: ${animationDuration}s;">
            </div>`;
    }

    rainContainer.innerHTML = drops;
};

makeItRain();

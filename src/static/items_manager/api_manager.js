export async function call_api(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);

        if (!response.ok) {
            // Gestion des erreurs HTTP
            throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
        }

        // Parse la réponse JSON
        const result = await response.json();
        return result;

    } catch (error) {
        // Affichage des erreurs dans la console et gestion supplémentaire
        console.error('API call failed:', error);
        return {
            success: false,
            message: error.message
        };
    }
}

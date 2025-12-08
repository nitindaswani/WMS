const CONFIG = {
    // Check if running on localhost or 127.0.0.1
    // If yes, use local API. Else, use Production API.
    // ACTION REQUIRED: Replace the URL below with your actual Render Backend URL after deployment.
    // Example: https://wms-backend.onrender.com/api
    API_BASE_URL: (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
        ? 'http://127.0.0.1:8000/api'
        : 'https://YOUR-RENDER-APP-URL.onrender.com/api'
};

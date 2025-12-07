const CONFIG = {
    // Check if running on localhost or 127.0.0.1
    // If yes, use local API. Else, use Production API.
    // ACTION REQUIRED: Replace the URL below with your actual Railway Backend URL after deployment.
    // Example: https://wms-backend.up.railway.app/api
    API_BASE_URL: (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
        ? 'http://127.0.0.1:8000/api'
        : 'https://YOUR-RAILWAY-APP-URL.up.railway.app/api'
};

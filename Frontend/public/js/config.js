const CONFIG = {
    // Check if running on localhost or 127.0.0.1
    // If yes, use local API. Else, use Production API.
    // REPLACE 'YOUR_RENDER_URL' with the actual URL provided by Render dashboard after deployment.
    // Example: https://wms-backend.onrender.com/api
    // Check if running on localhost or 127.0.0.1
    // If yes, use local API. Else, use Production API (PythonAnywhere).
    API_BASE_URL: (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
        ? 'http://127.0.0.1:8000/api'
        : 'https://khushsoni825.pythonanywhere.com/api'
};

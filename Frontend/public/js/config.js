/**
 * Global Configuration
 * 
 * Auto-detects environment:
 * - Localhost -> Local Backend
 * - Production -> PythonAnywhere Backend
 */

const getApiBaseUrl = () => {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://127.0.0.1:8000/api';
    }
    return 'https://nitindaswani2025.pythonanywhere.com/api';
};

const CONFIG = {
    API_BASE_URL: getApiBaseUrl()
};

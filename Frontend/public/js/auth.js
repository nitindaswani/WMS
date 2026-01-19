/**
 * Auth Service (JWT Edition)
 * Handles Token Management (Access/Refresh) and Requests.
 */
class Auth {
    static getAccessToken() { return localStorage.getItem('access_token'); }
    static getRefreshToken() { return localStorage.getItem('refresh_token'); }
    static getUser() {
        const user = localStorage.getItem('user');
        try {
            return user ? JSON.parse(user) : null;
        } catch (e) {
            return null;
        }
    }
    static getRole() { return localStorage.getItem('user_role'); }

    static isAuthenticated() {
        return !!this.getAccessToken();
    }

    /**
     * Login: Fetches JWT Pair
     */
    static async login(email, password) {
        try {
            const res = await fetch(`${CONFIG.API_BASE_URL}/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }) // Using 'email' as username field if backend expects it, or map appropriately
            });

            if (res.ok) {
                const data = await res.json();
                this.setSession(data);

                // Fetch User Profile to get Role/Name
                await this.fetchProfile();
                return { success: true };
            } else {
                return { success: false, error: 'Invalid credentials' };
            }
        } catch (e) {
            console.error("Login Error:", e);
            return { success: false, error: 'Network error' };
        }
    }

    static setSession(data) {
        if (data.access) localStorage.setItem('access_token', data.access);
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh);
    }

    static async fetchProfile() {
        // We assume an endpoint exists to get the current user details
        const res = await this.authenticatedFetch(`${CONFIG.API_BASE_URL}/auth/user/`);
        if (res.ok) {
            const user = await res.json();
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('user_role', user.role || 'student');
            localStorage.setItem('user_full_name', user.full_name || 'User');
        }
    }

    static logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_full_name');
        window.location.href = '/index.html';
    }

    /**
     * Authenticated Fetch Wrapper
     * auto-refreshes token on 401
     */
    static async authenticatedFetch(url, options = {}) {
        let token = this.getAccessToken();

        let headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        };

        let response = await fetch(url, { ...options, headers });

        // If 401, try to refresh
        if (response.status === 401) {
            console.log("Token expired, attempting refresh...");
            const refreshSuccess = await this.refreshToken();

            if (refreshSuccess) {
                // Retry with new token
                token = this.getAccessToken();
                headers['Authorization'] = `Bearer ${token}`;
                response = await fetch(url, { ...options, headers });
            } else {
                // Refresh failed
                this.logout();
                return response;
            }
        }

        return response;
    }

    static async refreshToken() {
        const refresh = this.getRefreshToken();
        if (!refresh) return false;

        try {
            const res = await fetch(`${CONFIG.API_BASE_URL}/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
            });

            if (res.ok) {
                const data = await res.json();
                localStorage.setItem('access_token', data.access);
                // Some backends rotate refresh tokens too
                if (data.refresh) localStorage.setItem('refresh_token', data.refresh);
                return true;
            }
        } catch (e) {
            console.error("Refresh Logic Error:", e);
        }
        return false;
    }
}

// Global Export
window.Auth = Auth;

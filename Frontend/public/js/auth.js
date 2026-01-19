/**
 * Authentication Helper
 * Handles login, logout, and authenticated requests.
 */

    },

// Get token
getToken: () => {
    return localStorage.getItem('auth_token');
},

    // Get role
    getRole: () => {
        return localStorage.getItem('auth_role');
    },

        // Remove session
        clearSession: () => {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('auth_role');
            localStorage.removeItem('user_full_name');
        },

            // Check if user is logged in
            isAuthenticated: () => {
                return !!localStorage.getItem('auth_token');
            },

                // Login function
                login: async (email, password, role) => {
                    try {
                        const body = { username: email, password };
                        if (role) body.role = role;

                        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(body),
                        });

                        const data = await response.json();

                        if (!response.ok) {
                            // If the error suggests "Invalid credentials", we should return that cleanly.
                            const errorMsg = data.non_field_errors ? data.non_field_errors[0] : (data.error || 'Login failed');
                            throw new Error(errorMsg);
                        }

                        // Expecting: { token: '...', user_id: 1, email: '...', role: 'student' }
                        if (data.token) {
                            const userRole = data.role || 'student';
                            Auth.setSession(data.token, userRole, data.full_name);
                            return { success: true, role: userRole };
                        } else {
                            return { success: false, error: 'No token received from server' };
                        }

                    } catch (error) {
                        return { success: false, error: error.message };
                    }
                },

                    // Signup function
                    signup: async (userData) => {
                        try {
                            const response = await fetch(`${CONFIG.API_BASE_URL}/auth/signup/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(userData),
                            });

                            const data = await response.json();

                            if (!response.ok) {
                                // Handle different types of errors (e.g., validation errors)
                                let errorMsg = 'Signup failed';
                                if (data.email) errorMsg = `Email: ${data.email[0]}`;
                                else if (data.password) errorMsg = `Password: ${data.password[0]}`;
                                else if (data.error) errorMsg = data.error;

                                throw new Error(errorMsg);
                            }

                            if (data.token) {
                                const role = data.user.role || userData.role || 'student';
                                const fullName = data.user.full_name || userData.full_name;
                                Auth.setSession(data.token, role, fullName);
                                return { success: true, role: role };
                            } else {
                                return { success: true, role: userData.role }; // Just created, maybe no token? But SignupView returns token.
                            }

                        } catch (error) {
                            return { success: false, error: error.message };
                        }
                    },

                        // Logout function
                        logout: () => {
                            const role = Auth.getRole();
                            Auth.clearSession();
                            if (role === 'admin') {
                                window.location.href = '/admin/login.html';
                            } else {
                                window.location.href = '/user/login.html';
                            }
                        },

                            // Helper to get dashboard URL based on role
                            getDashboardURL: (role) => {
                                switch (role) {
                                    case 'admin': return '/admin/dashboard.html'; // Assuming admin folder structure
                                    case 'speaker': return '/user/speaker-dashboard.html';
                                    case 'student': return '/user/dashboard.html';
                                    default: return '/user/dashboard.html';
                                }
                            },

                                // Wrapper for fetch that adds the Authorization header
                                authenticatedFetch: async (url, options = {}) => {
                                    const token = Auth.getToken();

                                    const headers = {
                                        'Content-Type': 'application/json',
                                        ...options.headers,
                                    };

                                    if (token) {
                                        headers['Authorization'] = `Token ${token}`;
                                    }

                                    const config = {
                                        ...options,
                                        headers,
                                    };

                                    const response = await fetch(url, config);

                                    if (response.status === 401) {
                                        // Token expired or invalid
                                        Auth.logout();
                                    }

                                    return response;
                                }
};


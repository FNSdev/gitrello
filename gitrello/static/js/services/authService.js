class AuthService {
    constructor() {
        this.token = this.getToken();
    }

    getToken() {
        return window.localStorage.getItem('Token');
    }

    setToken(token) {
        window.localStorage.setItem('Token', token);
    }

    isAuthenticated() {
        return this.token != null;
    }
}

export const authService = new AuthService();

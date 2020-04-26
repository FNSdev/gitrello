class AuthService {
    constructor() {
        this._token = this.getToken();
        this._user = null;
    }

    getToken() {
        return window.localStorage.getItem('Token');
    }

    _setToken(token) {
        window.localStorage.setItem('Token', token);
        this._token = token;
    }

    isAuthenticated() {
        return this._token != null;
    }

    getUser() {
        return this._user;
    }

    setUser(user) {
        this._user = user;
        this._setToken(user.token);
    }
}

export const authService = new AuthService();

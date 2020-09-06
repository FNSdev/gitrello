class TokenService {
    TOKEN = 'Token';
    JWT_TOKEN = 'JWT-Token'

    constructor() {
        this._token = window.localStorage.getItem(this.TOKEN);
        this._jwtToken = window.localStorage.getItem(this.JWT_TOKEN);
    }

    get token() {
        return this._token;
    }

    set token(value) {
        if (value == null) {
            window.localStorage.removeItem(this.TOKEN);
        }
        else {
            window.localStorage.setItem(this.TOKEN, value);
        }
        this._token = value;
    }

    get jwtToken() {
        return this._jwtToken;
    }

    set jwtToken(value) {
        if (value == null) {
            window.localStorage.removeItem(this.JWT_TOKEN);
        }
        else {
            window.localStorage.setItem(this.JWT_TOKEN, value);
        }
        this._jwtToken = value;
    }
}

export const tokenService = new TokenService();

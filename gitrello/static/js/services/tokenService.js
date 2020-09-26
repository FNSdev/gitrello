class TokenService {
    TOKEN_KEY = 'TOKEN';

    constructor() {
        this._token = window.localStorage.getItem(this.TOKEN_KEY);
    }

    get token() {
        return this._token;
    }

    set token(value) {
        if (value == null) {
            window.localStorage.removeItem(this.TOKEN_KEY);
        }
        else {
            window.localStorage.setItem(this.TOKEN_KEY, value);
        }
        this._token = value;
    }
}

export const tokenService = new TokenService();

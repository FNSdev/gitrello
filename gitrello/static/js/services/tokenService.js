class TokenService {
    constructor() {
        this._token = window.localStorage.getItem('Token');
    }

    get token() {
        return this._token;
    }

    set token(value) {
        if (value == null) {
            window.localStorage.removeItem('Token');
        }
        else {
            window.localStorage.setItem('Token', value);
        }
        this._token = value;
    }
}

export const tokenService = new TokenService();

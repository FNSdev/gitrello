export class GITrelloError extends Error {
    static defaultMessage = 'Oops. Something went wrong on our side. Please, try again.';

    constructor(message = null) {
        if (message === null) {
            message = GITrelloError.defaultMessage;
        }

        super(message);
    }
}


export class RepositoryError extends GITrelloError {
    constructor(message) {
        super(message);
    }
}


export class HttpClientError extends GITrelloError {
    constructor(message) {
        super(message);
    }
}


export class HttpClientBadRequestError extends HttpClientError {
    constructor(message, errors) {
        super(message);
        this.errors = errors;  // TODO I dont want to parse them and show separately for each input :C
    }
}


export class HttpClientPermissionDeniedError extends HttpClientError {
    constructor(message) {
        super(message);
    }
}

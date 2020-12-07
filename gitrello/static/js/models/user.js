export class User {
    constructor({id, addedAt, token, username, email, firstName, lastName}) {
        this.id = id;
        this.addedAt = addedAt;
        this.token = token;
        this.username = username;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
    }
}

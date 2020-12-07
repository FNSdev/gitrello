export class OrganizationInvite {
    constructor({id, addedAt, user, message, organization}) {
        this.id = id;
        this.addedAt = addedAt;
        this.user = user;
        this.message = message;
        this.organization = organization;
    }
}

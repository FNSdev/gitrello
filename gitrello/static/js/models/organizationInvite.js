export class OrganizationInvite {
    constructor({id, addedAt, user, message, status, organization}) {
        this.id = id;
        this.addedAt = addedAt;
        this.user = user;
        this.message = message;
        this.status = status;
        this.organization = organization;
    }
}

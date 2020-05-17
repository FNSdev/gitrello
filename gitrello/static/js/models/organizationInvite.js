export class OrganizationInvite {
    constructor({id, added_at, user, message, status, organization}) {
        this.id = id;
        this.added_at = added_at;
        this.user = user;
        this.message = message;
        this.status = status;
        this.organization = organization;
    }
}

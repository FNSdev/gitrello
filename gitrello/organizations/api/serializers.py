from rest_framework import serializers

from boards.api.serializers import BoardMembershipSerializer, BoardSerializer, NestedOrganizationMembershipSerializer
from organizations.models import Organization, OrganizationMembership, OrganizationInvite


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CreateOrganizationInviteSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()


class UpdateOrganizationInviteSerializer(serializers.Serializer):
    accept = serializers.BooleanField()


class NestedOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'added_at', 'name')

    id = serializers.CharField()


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = (
            'id',
            'role',
            'organization',
            'board_memberships',
        )

    id = serializers.CharField()
    organization = NestedOrganizationSerializer(read_only=True)
    board_memberships = BoardMembershipSerializer(many=True, read_only=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'added_at', 'name', 'organization_memberships', 'boards')

    id = serializers.CharField()
    organization_memberships = NestedOrganizationMembershipSerializer(many=True, read_only=True)
    boards = BoardSerializer(many=True, read_only=True)


class OrganizationInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = ('id', 'message', 'status', 'added_at', 'organization')

    id = serializers.CharField()
    organization = NestedOrganizationSerializer(read_only=True)

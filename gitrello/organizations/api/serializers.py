from rest_framework import serializers

from boards.api.serializers import BoardMembershipSerializer
from organizations.models import Organization, OrganizationMembership


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CreateOrganizationInviteSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()


class UpdateOrganizationInviteSerializer(serializers.Serializer):
    accept = serializers.BooleanField()


class OrganizationSerializer(serializers.ModelSerializer):
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
    organization = OrganizationSerializer(read_only=True)
    board_memberships = BoardMembershipSerializer(many=True, read_only=True)

from rest_framework import serializers

from organizations.choices import OrganizationMemberRole
from organizations.models import Organization, OrganizationInvite, OrganizationMembership


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CreateOrganizationInviteSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()


class UpdateOrganizationInviteSerializer(serializers.Serializer):
    accept = serializers.BooleanField()


class UpdateOrganizationMembershipSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=(
            OrganizationMemberRole.ADMIN,
            OrganizationMemberRole.MEMBER,
        ),
    )


class CreateOrganizationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')

    id = serializers.CharField()


class CreateOrganizationInviteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = ('id', 'user_id', 'organization_id', 'message')

    id = serializers.CharField()
    user_id = serializers.CharField()
    organization_id = serializers.CharField()


class UpdateOrganizationMembershipResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = ('id', 'user_id', 'organization_id', 'role')

    id = serializers.CharField()

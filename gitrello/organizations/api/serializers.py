from rest_framework import serializers

from organizations.models import Organization, OrganizationInvite


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CreateOrganizationInviteSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()


class UpdateOrganizationInviteSerializer(serializers.Serializer):
    accept = serializers.BooleanField()


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

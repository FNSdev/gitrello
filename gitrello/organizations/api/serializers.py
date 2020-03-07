from rest_framework import serializers


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CreateOrganizationInviteSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    email = serializers.EmailField()
    message = serializers.CharField()


class UpdateOrganizationInviteSerializer(serializers.Serializer):
    accept = serializers.BooleanField()

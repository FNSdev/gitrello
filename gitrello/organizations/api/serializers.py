from rest_framework import serializers


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

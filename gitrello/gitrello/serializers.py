from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    error_code = serializers.IntegerField()
    error_message = serializers.CharField()
    error_details = serializers.JSONField(required=False)

from rest_framework import serializers


class CreateTicketSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()

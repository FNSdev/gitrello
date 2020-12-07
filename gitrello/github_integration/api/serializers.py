from rest_framework import serializers


class CreateTicketSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    body = serializers.CharField(allow_blank=True)

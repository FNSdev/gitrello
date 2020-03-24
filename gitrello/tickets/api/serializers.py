from rest_framework import serializers


class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    board_id = serializers.IntegerField()

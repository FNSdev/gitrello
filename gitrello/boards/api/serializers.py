from authentication.api.serializers import UserSerializer
from boards.models import Board, BoardMembership

from rest_framework import serializers


class CreateBoardSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class CreateBoardMembershipSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    organization_membership_id = serializers.IntegerField()


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name')

    id = serializers.CharField()


class BoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ('id', 'user', 'board')

    id = serializers.CharField()
    board = BoardSerializer(read_only=True)
    user = UserSerializer(read_only=True)

from rest_framework import serializers

from boards.models import Board, BoardMembership


class CreateBoardSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class CreateBoardMembershipSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    organization_membership_id = serializers.IntegerField()


class GetBoardPermissionsSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


class CreateBoardResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'organization_id')

    id = serializers.CharField()
    organization_id = serializers.CharField()


class CreateBoardMembershipResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ('id', 'board_id', 'organization_membership_id')

    id = serializers.CharField()
    board_id = serializers.CharField()
    organization_membership_id = serializers.CharField()

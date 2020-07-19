from rest_framework import serializers


class CreateBoardSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class CreateBoardMembershipSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    organization_membership_id = serializers.IntegerField()

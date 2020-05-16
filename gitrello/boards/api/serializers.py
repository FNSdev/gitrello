from authentication.api.serializers import UserSerializer
from boards.models import Board, BoardMembership
from organizations.models import OrganizationMembership

from rest_framework import serializers


class CreateBoardSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class CreateBoardMembershipSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    organization_membership_id = serializers.IntegerField()


class NestedOrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = (
            'id',
            'role',
            'user',
        )

    id = serializers.CharField()
    user = UserSerializer(read_only=True)


class NestedBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name')

    id = serializers.CharField()


class BoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ('id', 'organization_membership', 'board')

    id = serializers.CharField()
    board = NestedBoardSerializer(read_only=True)
    organization_membership = NestedOrganizationMembershipSerializer(read_only=True)


class NestedBoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ('id', 'organization_membership')

    id = serializers.CharField()
    organization_membership = NestedOrganizationMembershipSerializer(read_only=True)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'board_memberships')

    id = serializers.CharField()
    board_memberships = NestedBoardMembershipSerializer(many=True, read_only=True)

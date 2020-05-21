from rest_framework import serializers

from authentication.api.serializers import UserSerializer
from boards.models import BoardMembership
from organizations.models import OrganizationMembership
from tickets.models import Category, Ticket, TicketAssignment


class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    board_id = serializers.IntegerField()


class CreateTicketSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()


class UpdateTicketSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, allow_null=True, required=False)
    body = serializers.CharField(allow_null=True, required=False)
    due_date = serializers.DateField(allow_null=True, required=False)


class CreateTicketAssignmentSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    board_membership_id = serializers.IntegerField()


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = (
            'id',
            'role',
            'user',
        )

    id = serializers.CharField()
    user = UserSerializer(read_only=True)


class BoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ('id', 'added_at', 'organization_membership')

    id = serializers.CharField()
    organization_membership = OrganizationMembershipSerializer(read_only=True)


class TicketAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAssignment
        fields = ('id', 'added_at', 'assignee')

    id = serializers.CharField()
    assignee = BoardMembershipSerializer(read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'added_at', 'title', 'body', 'due_date', 'assignments')

    id = serializers.CharField()
    assignments = TicketAssignmentSerializer(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'added_at', 'name', 'tickets')

    id = serializers.CharField()
    tickets = TicketSerializer(many=True, read_only=True)

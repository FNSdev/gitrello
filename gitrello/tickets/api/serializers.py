from rest_framework import serializers

from tickets.models import Category, Comment, Ticket, TicketAssignment


class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    board_id = serializers.IntegerField()


class UpdateCategoryNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class MoveCategoryActionSerializer(serializers.Serializer):
    insert_after_category_id = serializers.IntegerField(allow_null=True)


class CreateTicketSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()


class UpdateTicketSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, allow_null=True, required=False)
    body = serializers.CharField(allow_null=True, required=False)
    due_date = serializers.DateField(allow_null=True, required=False)


class MoveTicketActionSerializer(serializers.Serializer):
    insert_after_ticket_id = serializers.IntegerField(allow_null=True)
    category_id = serializers.IntegerField()


class CreateTicketAssignmentSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    board_membership_id = serializers.IntegerField()


class CreateCommentSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    message = serializers.CharField()


class CreateCategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'board_id', 'name', 'priority')

    id = serializers.CharField()
    board_id = serializers.CharField()


class UpdateCategoryNameResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'board_id', 'name', 'priority')

    id = serializers.CharField()
    board_id = serializers.CharField()


class MoveCategoryActionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'priority')

    id = serializers.CharField()


class CreateTicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'category_id', 'priority')

    id = serializers.CharField()
    category_id = serializers.CharField()


class UpdateTicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'category_id', 'priority', 'title', 'body', 'due_date')

    id = serializers.CharField()
    category_id = serializers.CharField()


class MoveTicketActionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'category_id', 'priority')

    id = serializers.CharField()
    category_id = serializers.CharField()


class CreateTicketAssignmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAssignment
        fields = ('id', 'ticket_id', 'assignee_id')

    id = serializers.CharField()
    ticket_id = serializers.CharField()
    assignee_id = serializers.CharField()


class CreateCommentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'ticket_id', 'author_id', 'message', 'added_at')

    id = serializers.CharField()
    ticket_id = serializers.CharField()
    author_id = serializers.CharField()

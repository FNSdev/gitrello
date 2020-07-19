from graphene import Node


class GITrelloNode(Node):
    class Meta:
        name = 'Node'

    @classmethod
    def to_global_id(cls, type, id):
        return id

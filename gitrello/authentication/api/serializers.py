from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.models import User


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        user = User(
            username=attrs['username'],
            email=attrs['email'],
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
        )

        try:
            validate_password(password=attrs['password'], user=user)
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.messages)

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'added_at',
            'username',
            'email',
            'first_name',
            'last_name',
        )

    id = serializers.CharField()

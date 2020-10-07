from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.choices import OauthProvider
from authentication.models import OauthState, User
from authentication.services.permissions_service import Permissions


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


class CreateOauthStateSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=OauthProvider.CHOICES)


class CreateUserResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)
    token = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)
    token = serializers.CharField()


class AuthTokenOwnerResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=100)


class CreateOauthStateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthState
        fields = ('id', 'user_id', 'provider', 'state')

    id = serializers.CharField()
    user_id = serializers.CharField()


class PermissionsSerializer(serializers.Serializer):
    can_read = serializers.BooleanField()
    can_mutate = serializers.BooleanField()
    can_delete = serializers.BooleanField()

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    ERROR_ME_USERNAME_RESTRICTED = {
        'username': 'registration "me" username restricted'}

    class Meta:
        fields = ['email', 'username']
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                self.ERROR_ME_USERNAME_RESTRICTED
            )
        return value

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username', 'confirmation_code']
        model = User

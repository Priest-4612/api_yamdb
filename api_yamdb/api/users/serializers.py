from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    default_error_messages = {
        'username': ('Имя пользователя должно содержать только'
                     'буквенно-цифровые символы.')
    }

    class Meta:
        models = User
        fields = ['email', 'username']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)

        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password()
        user.save()
        return user

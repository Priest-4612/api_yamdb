from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'username': ('Имя пользователя должно содержать только'
                     'буквенно-цифровые символы.'),
        'email': ('адрес электронной почты уже используется ')
    }

    class Meta:
        models = User
        fields = ['email', 'username']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(self.default_error_messages)
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)

        return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)

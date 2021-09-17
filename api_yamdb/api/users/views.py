from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.serializers import RegisterSerializer, TokenSerializer
from users.models import User


class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            confirmation_code = default_token_generator.make_token(
                get_object_or_404(User, username=serializer.data['username'])
            )
            send_mail(
                subject='Регистрация нового пользователя',
                message=f'Ваш код {confirmation_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.data.get('email')]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        user = get_object_or_404(User, username=serializer.data['username'])
        if serializer.is_valid():
            token = default_token_generator.make_token(user)
            data = {'token': token}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

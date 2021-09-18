import jwt

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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
            user_data = serializer.data
            user = get_object_or_404(User, username=user_data['username'])
            confirmation_code = RefreshToken.for_user(user).access_token
            send_mail(
                subject='Регистрация нового пользователя',
                message=f'Ваш код {confirmation_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_data['email']]
            )
            return Response(user_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        decode_token = jwt.decode(
            confirmation_code, settings.SECRET_KEY, algorithms="HS256"
        )
        user = get_object_or_404(User, username=request.data.get('username'))
        if decode_token['user_id'] == user.id:
            token = RefreshToken.for_user(user).access_token
            data = {'token': str(token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
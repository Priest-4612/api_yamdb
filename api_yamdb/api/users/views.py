import jwt

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from api.users.permissions import AdminOnly, OwnerOnly
from api.users.serializers import (RegisterSerializer, TokenSerializer,
                                   UserSerializer, MeSerializer)
from users.models import User


class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        try:
            decode_token = jwt.decode(
                confirmation_code, settings.SECRET_KEY, algorithms="HS256"
            )
            if decode_token['user_id'] == user.id:
                token = RefreshToken.for_user(user)
                data = {'token': str(token.access_token)}
                return Response(data=data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as error:
            message = {'token_error': str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeViewSet(viewsets.ModelViewSet):
    permission_classes = [OwnerOnly]
    serializer_class = MeSerializer

    def retrieve(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user)
        serializer = MeSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user)
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user)
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

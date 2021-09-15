from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializers import RegisterSerializer
from users.models import User


class RegisterView(generics.CreateAPIView):
    queryset = User
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer

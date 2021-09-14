from functools import partialmethod
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import RegisterView

app_name = 'user'
router = DefaultRouter()


urlpatterns = [
    path('singup', RegisterView.as_view(), name='register')
]

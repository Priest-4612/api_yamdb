from functools import partialmethod
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.users.views import RegisterView

app_name = 'user'
router = DefaultRouter()


urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
]

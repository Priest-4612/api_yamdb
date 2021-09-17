from django.urls import path
from rest_framework.routers import DefaultRouter

from api.users.views import RegisterView, TokenView

app_name = 'user'
router = DefaultRouter()


urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('token/', TokenView.as_view(), name='token')
]

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router_B = DefaultRouter()
router_B.register('titles', TitleViewSet)
router_B.register('genres', GenreViewSet)
router_B.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router_B.urls)),
]

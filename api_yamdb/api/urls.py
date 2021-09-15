from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryDestroy, TitleViewSet, GenreList, GenreDestroy, CategoryList

router_B = DefaultRouter()
router_B.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_B.urls)),
    path('v1/genres/', GenreList.as_view()),
    path('v1/<slug:slug>/', GenreDestroy.as_view()),
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', CategoryDestroy.as_view()),
    path('v1/auth/', include('api.users.urls')),
]

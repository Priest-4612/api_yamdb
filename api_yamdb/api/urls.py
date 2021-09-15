from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet
from .views import (
    CategoryDestroy,
    TitleViewSet,
    GenreList,
    GenreDestroy,
    CategoryList,
)

router_C = DefaultRouter()
router_C.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
router_C.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

# urlpatterns = [
#    path('v1/', include(router_C.urls)),

router_B = DefaultRouter()
router_B.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include(router_B.urls)),
    path('v1/', include(router_C.urls)),
    path('v1/genres/', GenreList.as_view()),
    path('v1/genres/<slug:slug>/', GenreDestroy.as_view()),
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', CategoryDestroy.as_view()),
]

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoryDestroy, CategoryList, CommentViewSet,
                    GenreDestroy, GenreList, RegisterView, ReviewViewSet,
                    TitleViewSet, TokenView, UserViewSet)


router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('genres/', GenreList.as_view()),
    path('genres/<slug:slug>/', GenreDestroy.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<slug:slug>/', CategoryDestroy.as_view()),
    path('auth/signup/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenView.as_view(), name='token')
]

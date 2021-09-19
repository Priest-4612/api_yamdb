from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CommentViewSet,
    CategoryDestroy,
    TitleViewSet,
    GenreList,
    GenreDestroy,
    CategoryList,
    ReviewViewSet,
    UserViewSet,
    MeViewSet,
    RegisterView,
    TokenView
)

router_C = DefaultRouter()
router_C.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
router_C.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_B = DefaultRouter()
router_B.register('titles', TitleViewSet, basename='titles')

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

me_detail = MeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
    path('v1/', include(router_B.urls)),
    path('v1/', include(router_C.urls)),
    path('v1/genres/', GenreList.as_view()),
    path('v1/genres/<slug:slug>/', GenreDestroy.as_view()),
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', CategoryDestroy.as_view()),
    path('v1/auth/signup/', RegisterView.as_view(), name='register'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/users/me/', me_detail, name='me_detail'),
    path('v1/users/', user_list, name='user-list'),
    path('v1/users/<str:username>/', user_detail, name='user-detail'),
]

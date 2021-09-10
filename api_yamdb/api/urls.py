from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet

router_C = DefaultRouter()
router_C.register(r'titles/(?P<title_id>\d+)/reviews',
                  ReviewViewSet, basename='reviews')
router_C.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_C.urls)),
]

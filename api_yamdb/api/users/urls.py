from django.urls import path

from api.users import views

app_name = 'users'
user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


me_detail = views.MeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
    path('users/me/', me_detail, name='me_detail'),
    path('users/', user_list, name='user-list'),
    path('users/<str:username>/', user_detail, name='user-detail'),
    path('signup/', views.RegisterView.as_view(), name='register'),
    path('token/', views.TokenView.as_view(), name='token')
]

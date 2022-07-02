
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import UserCreateAPIView, UserRetrieveUpdateAPIView

app_name = 'user'

urlpatterns = [
    path('create/',UserCreateAPIView.as_view(),name=('create')),
    path('token/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserRetrieveUpdateAPIView.as_view(), name='me' ) # profile of user
]

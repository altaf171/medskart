
from django.urls import path
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
    path('me/', UserRetrieveUpdateAPIView.as_view(), name='me' )
]

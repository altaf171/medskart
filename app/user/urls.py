import imp
from django.urls import path

from user.views import UserCreateAPIView

app_name = 'user'

urlpatterns = [
    path('create/',UserCreateAPIView.as_view(),name=('create')),
]

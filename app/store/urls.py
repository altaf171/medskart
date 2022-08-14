from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    homePage
)

urlpatterns = [
    path('',homePage, name="home-page"),
    path('login/', auth_views.LoginView.as_view(template_name="store/login.html"), name="login")
    
]

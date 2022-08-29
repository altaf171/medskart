from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    homePage,
    ProfilePage
)

urlpatterns = [
    
    path('',homePage, name="home-page"),
    path("profile/", ProfilePage.as_view(), name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="store/logged_out.html"), name="logout"),
    
]

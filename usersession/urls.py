from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginRequest, name="login"),
    path('register/', views.registerRequest, name="register"),
    path('logout/', views.logoutRequest, name="logout"),

]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

urlpatterns = [
    path('', views.LandingView.as_view()),
    path('register/', views.UserRegView.as_view()),
    path('login/', views.LoginView.as_view()),
]

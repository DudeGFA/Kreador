from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
]

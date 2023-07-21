from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'userprofile'
urlpatterns = [
    path('like', views.PostLikeView.as_view()),
]

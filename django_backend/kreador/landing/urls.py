from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.LandingView.as_view()),
    path('register/', views.UserRegView.as_view()),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html',success_url='done/'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        TemplateView.as_view(template_name='password_reset/password_reset_done.html',),
        name='password_reset_done'
    ),
    path(
        'password_reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html', success_url='/password_reset/complete/'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/',
        TemplateView.as_view(template_name='password_reset/password_reset_complete.html',),
        name='password_reset_confirm'
    ),
]

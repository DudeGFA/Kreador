from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'userprofile'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='user_detail'),
    path('videos/', views.VideoView.as_view()),
    path('media/', views.MediaView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('connections/', views.ConnectionsView.as_view()),
    path('events/', views.EventsView.as_view()),
    path('activity/', views.ActivityView.as_view()),
    path('post/<int:pk>/delete',
        views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like',
        views.PostLikeView.as_view(), name='post_like'),
    path('post/<int:pk>/unlike',
        views.PostUnLikeView.as_view(), name='post_unlike'),
    path('comment/post/<int:pk>',
        views.PostCommentView.as_view(), name='post_comment'),
    path('contacts/add/<int:pk>',
        views.AddContactView.as_view(), name='del_contact'),
    path('contacts/del/<int:pk>',
        views.DeleteContactView.as_view(), name='add_contact'),
]

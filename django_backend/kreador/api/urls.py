from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('comment/like/', views.CommentLikeView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('reply/like/', views.ReplyLikeView.as_view()),
    path('replies/', views.ReplyList.as_view()),
    path('replies/<int:pk>/', views.ReplyDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
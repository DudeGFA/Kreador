from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', views.PostViewSet,basename="post")
router.register(r'users', views.UserViewSet,basename="user")
router.register(r'polls', views.PollViewSet,basename="poll")
router.register(r'profiles', views.UserProfileViewSet,basename="profile")

urlpatterns = [
    path('', include(router.urls)),
    path('comment/like/', views.CommentLikeView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('reply/like/', views.ReplyLikeView.as_view()),
    path('replies/', views.ReplyList.as_view()),
    path('replies/<int:pk>/', views.ReplyDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

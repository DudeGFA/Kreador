from userprofile.models import Comment, Reply, CommentLike
from rest_framework import serializers
from django.contrib.auth.models import User
from userprofile.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    #profilepic = serializers.CharField()
    class Meta:
        model = Profile
        fields = ['image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    username = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile']

class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    reply_count = serializers.IntegerField(
    source='reply_set.count', 
    read_only=True
)
    like_count = serializers.IntegerField(
    source='commentlike_set.count', 
    read_only=True
)
    #imageurl = serializers.CharField(required=True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'owner', 'created_at', 'like_count', 'reply_count']

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'comment']

class ReplySerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    like_count = serializers.IntegerField(
    source='replylike_set.count', 
    read_only=True
)
    class Meta:
        model = Reply
        fields = ['id', 'text', 'comment', 'owner', 'created_at', 'like_count']
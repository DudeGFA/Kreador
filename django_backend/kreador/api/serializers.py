from userprofile.models import Comment, Reply, CommentLike, ReplyLike, Post, Poll
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

class UserIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = ['id']

class GetUserSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    class Meta:
        model = Profile
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    owner = UserSerializer(required=False)
    reply_count = serializers.IntegerField(
    source='reply_set.count',
    read_only=True
)
    like_count = serializers.IntegerField(
    source='commentlike_set.count',
    read_only=True
)
    liked = serializers.SerializerMethodField()
    #imageurl = serializers.CharField(required=True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'owner', 'created_at', 'like_count', 'reply_count', 'liked']

    def get_liked(self, obj):
        try:
            #print(self.context["request"].user)
            if CommentLike.objects.filter(user=self.context["request"].user, comment=obj).exists():
                return True
        except Exception as e:
            print(e)
        return False

class CommentLikeSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    user = UserIdSerializer(required=False, read_only=True)
    like_count = serializers.IntegerField(
    source='comment.commentlike_set.count',
    read_only=True
)
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'like_count']

class ReplySerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    owner = UserSerializer(required=False)
    like_count = serializers.IntegerField(
    source='replylike_set.count',
    read_only=True
)
    like_count = serializers.IntegerField(
    source='replylike_set.count',
    read_only=True
)
    liked = serializers.SerializerMethodField()
    def get_liked(self, obj):
        try:
            #print(self.context["request"].user)
            if ReplyLike.objects.filter(user=self.context["request"].user, reply=obj).exists():
                return True
        except Exception as e:
            print(e)
        return False

    class Meta:
        model = Reply
        fields = ['id', 'text', 'comment', 'owner', 'created_at', 'like_count', 'liked']

class ReplyLikeSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    user = UserIdSerializer(required=False, read_only=True)
    like_count = serializers.IntegerField(
    source='reply.replylike_set.count',
    read_only=True
)
    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'reply', 'like_count']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    class Meta:
        model = Post
        fields = '__all__'

class PollSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    class Meta:
        model = Poll
        fields = '__all__'
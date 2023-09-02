from django import forms

from .models import Post, Comment, Reply, Profile, PostImage
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','video')

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('text',)

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name"]


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['occupation', 'dob', 'country', 'city', 'status', 'about',]


class UpdateProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class UpdateProfileBackgroundPhotoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['background_photo']
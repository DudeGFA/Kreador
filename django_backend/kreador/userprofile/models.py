from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.conf import settings
from datetime import datetime
from django.core.validators import FileExtensionValidator
from  business.models import Business

class Profile(models.Model):
    """User's profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg',  
                                     upload_to='profile_pics')
    background_photo = models.ImageField(default='background_photos/default.jpg',  
                                     upload_to='background_photos')
    city = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)
    occupation = models.CharField(max_length=50, null=True)
    about = models.CharField(max_length=250, null=True)
    dob = models.DateField(null=True)
    contacts = models.ManyToManyField(User, blank=True, through='Usercontact', related_name="contacted_by")
    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    """Post object"""
    text = models.TextField()
    video = models.FileField(upload_to='post_videos',null=True,
                                     validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Postlike', related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.owner.username} Post({self.id})'

class PostImage(models.Model):
    image = models.ImageField(null=True,  upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserExperience(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    enterprise = models.ForeignKey(Business, blank=True, null=True, on_delete=models.SET_NULL)
    enterprise_name = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

class Reply(models.Model) :
    text = models.TextField(max_length=200)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostLike(models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} Like post {self.post.owner}({self.post.id})'

class CommentLike(models.Model) :
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('comment', 'user')

class ReplyLike(models.Model) :
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('reply', 'user')

class UserContact(models.Model) :
    profile = models.ForeignKey(Profile,  on_delete=models.PROTECT)
    contact = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile', 'contact')

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from userprofile.models import Post, PostLike

@method_decorator(csrf_exempt, name='dispatch')
class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, post_id) :
        print("Add like to post", post_id)
        liked_post = get_object_or_404(Post, id=post_id)
        post_like = PostLike(user=request.user, post=liked_post)
        try:
            post_like.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()
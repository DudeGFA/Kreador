from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Post, Profile, Poll
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from itertools import chain
from django.db.models import Count, F
# Create your views here.

class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        posts = Post.objects.filter(owner__in=request.user.profile.contacts.all()).order_by('-created_at')
        polls = Poll.objects.filter(owner__in=request.user.profile.contacts.all())
        feed = sorted(chain(posts, polls), key=lambda feedobj: feedobj.created_at, reverse=True)
        contacts = list(User.objects.all())

        for user in list(User.objects.all()):
            if request.user.profile.contacts.filter(username=user.username).exists():
                contacts.remove(user)
        if request.user in contacts:
            contacts.remove(request.user)

        mutualconnections = User.objects.filter(contacted_by__user__in=request.user.profile.contacts.all()).exclude(profile__user__in=request.user.profile.contacts.all())
        mutualconnections = mutualconnections.exclude(pk=request.user.id)
        mutualconnectionswithcount = mutualconnections.values().annotate(mccount=Count('id'), image_url=F('profile__image')).order_by('-mccount')
        ctx = {'feed': feed, 'contacts_to_add': contacts[:4], 'mutualconnections': mutualconnectionswithcount}
        return render(request, 'home_modified/user_index.html', ctx)
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Post, Profile
from django.contrib.auth.models import User

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        feed = []
        for contact in request.user.profile.contacts.all():
            feed += contact.post_set.all()
        #print(feed)
        contacts = list(User.objects.all())
        print(contacts)
        print(list(request.user.profile.contacts.all()))
        for user in list(User.objects.all()):
            print(user)
            if request.user.profile.contacts.filter(username=user.username).exists():
                print('removed ', user)
                contacts.remove(user)
        if request.user in contacts:
            contacts.remove(request.user)
        print(contacts)
        print(request.user.contacted_by.all())
        ctx = {'feed': feed, 'contacts_to_add': contacts[:4]}
        return render(request, 'home_modified/user_index.html', ctx)
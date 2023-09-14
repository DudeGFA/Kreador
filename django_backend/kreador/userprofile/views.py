"""
    Contains djangoo class based views
    That handle requests related to:
        User's profile - ProfileView.get
        Post Create - ProfileView.post
        Post Delete - PostDeleteView
        Post Comment - PostCommentView
        Add Contacts - AddContactsView
        Delete Contact - DeleteContactView
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, UserContact, PostImage, PostLike, Poll, PollOption, Voter, Profile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from .forms import PostForm, CommentForm, ReplyForm, UpdateProfileForm, UpdateUserForm
from .forms import UpdateProfileBackgroundPhotoForm, UpdateProfileImageForm, PostImageForm, PollForm, PollOptionForm
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
import json
from django.core.files.images import ImageFile
from copy import copy
from landing.forms import NewUserForm
import time
from itertools import chain
# Create your views here.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        """ Handles get request for a user's profile
            Args:
                request: GET request object
                username (str): username of user profile requested
            Return: web page of < username >'s profile
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        post_list = Post.objects.filter(owner=user).order_by('-updated_at')
        polls = Poll.objects.filter(owner=user).order_by('-created_at')
        feed = sorted(chain(post_list, polls), key=lambda feedobj: feedobj.created_at, reverse=True)
        album = PostImage.objects.filter(post__owner=user)
        #print('album:', album)
        ctx = {'month_joined': month_joined, 'post_list': feed, 'profile_owner': user, 'album': album}
        #print(post_list[1].comment_set.all())
        return render(request, 'home_modified/user_profile.html', ctx)

    def post(self, request, username):
        """ Handles Creation of new post
            Args:
                request: post request object
                username (str) : username of post request sender
            Returns: Redirect url after saving the post
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        next = request.POST.get('next', '/home')
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.owner = self.request.user
            new_post.save()
        else:
            print(post_form.errors)
            return HttpResponseRedirect(next)
        # new_post = Post.objects.create(text=request.POST.get('text'), owner=user)
        # new_post.save()
        # if request.FILES.getlist('video'):
        #     # saves video file
        #     new_post.video = request.FILES.getlist('video')[0]
        #     new_post.save()
        if request.FILES.getlist('picture[0]'):
            # creates and saves post image
            for key in request.FILES.keys():
                #loops through each uploaded image file
                if key.startswith('picture'):
                    value=request.FILES.getlist(key)[0]
                    post_img_form = PostImageForm(request.POST, {'image': value})
                    if post_img_form.is_valid():
                        new_post_img = post_img_form.save(commit=False)
                        new_post_img.post = new_post
                        new_post_img.save()
                    else:
                        print(post_img_form.errors)
        #post_form = PostForm(request.POST, request.FILES or None)

        #if not post_form.is_valid():
        #    return HttpResponse('Invalid form')

        # Add owner to the model before saving
        #saved_form = post_form.save(commit=False)
        #saved_form.owner = user
        #saved_form.save()
        #post_form.save_m2m()
        #redirects to the value of next form attribute
        return HttpResponseRedirect(next)

class PollView(LoginRequiredMixin, View):
    """Handles Poll creation"""
    def post(self, request, username):
        """Creates a new Poll object
            Args:
                request: post request object
                username (str) : username of post request sender
            Returns: Redirect url after saving the post
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        next = request.POST.get('next', '/home')
        polloptions = [request.POST.get('firstoption'), request.POST.get('secondoption'), request.POST.get('thirdoption'), request.POST.get('fourthoption')]
        validpolloptions = []
        for polloption in polloptions:
            if polloption:
                validpolloptions.append(polloption)
        if len(validpolloptions) < 2:
            return HttpResponse('Invalid Poll')
        new_poll_form = PollForm(request.POST)
        if new_poll_form.is_valid():
            new_poll = new_poll_form.save(commit=False)
            new_poll.owner = request.user
            new_poll.save()
        else:
            return HttpResponse('Invalid Poll')
        for i in range(len(validpolloptions)):
            index = i + 1
            newpolloptionform = PollOptionForm({'text':validpolloptions[i], 'index': index})
            if newpolloptionform.is_valid():
                newpolloption = newpolloptionform.save(commit=False)
                newpolloption.poll = new_poll
                newpolloption.save()
            else:
                return HttpResponse('Poll option ' + index + ' is invalid')
        #redirects to the value of next form attribute
        return HttpResponseRedirect(next)

@method_decorator(csrf_exempt, name='dispatch')
class PollVoteView(LoginRequiredMixin, View):
    def post(self, request, username, optionid):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        try:
            Choice = PollOption.objects.get(pk=optionid)
        except PollOption.DoesNotExist:
            return HttpResponse('Poll does not exist')
        if not Voter.objects.filter(polloption__poll__id=Choice.poll.id, voter=user):
            voter = Voter.objects.create(polloption=Choice, voter=user)
            voter.save()
        totalvotes = Voter.objects.filter(polloption__poll__id=Choice.poll.id).count()
        response = {}
        for option in Choice.poll.polloption_set.all():
            votepercentage = (option.voters.count() / totalvotes) * 100
            response[option.id] = str(votepercentage)
        response['totalvotes'] = totalvotes
        print(JsonResponse(response, safe=False))
        return JsonResponse(response, safe=False)

class PostDeleteView(LoginRequiredMixin, View):
    """
        Deletes a post
    """
    def post(self, request, pk, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist', status=404)
        try:
            post_obj = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponse('Post object does not exist')

        if request.user != user or request.user != post_obj.owner:
            return HttpResponse('User not authorized', status=404)
        post_obj.delete()
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, username) :
        print("Add like to post", pk)
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        liked_post = get_object_or_404(Post, id=pk)
        try:
            post_like = PostLike.objects.create(user=request.user, post=liked_post)
            post_like.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class PostUnLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, username) :
        print("Unlike post", pk)
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        unliked_post = get_object_or_404(Post, id=pk)
        try:
            post_unlike = PostLike.objects.get(user=request.user, post=unliked_post)
            post_unlike.delete()  # In case of duplicate key
        except ObjectDoesNotExist as e:
            pass
        return HttpResponse()

class PostCommentView(LoginRequiredMixin, View):
    """
        Handles posting a comment
    """
    def post(self, request, username, pk):
        """
            Creates a new Comment object
            Returns: a redirect to a next parameter
        """
        print(request.POST)
        comment_form = CommentForm(request.POST)

        if not comment_form.is_valid():
            return HttpResponse('Invalid comment form')

        # Add owner to the model before saving
        saved_form = comment_form.save(commit=False)
        saved_form.owner = request.user
        saved_form.post = get_object_or_404(Post, id=pk)
        saved_form.save()
        comment_form.save_m2m()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        #return redirect('/' + username)

class PostReplyView(LoginRequiredMixin, View):
    """
        Handles posting a reply
    """
    def post(self, request, username, pk):
        """
            Creates a new Reply object
            Returns: a redirect to a next parameter
        """
        #print(request.POST)
        reply_form = ReplyForm(request.POST)

        if not reply_form.is_valid():
            return HttpResponse('Invalid reply form')

        # Add owner to the model before saving
        saved_form = reply_form.save(commit=False)
        saved_form.owner = request.user
        saved_form.comment = get_object_or_404(Comment, id=pk)
        saved_form.save()
        reply_form.save_m2m()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        #return redirect('/' + username)

# class VideoView(LoginRequiredMixin, View):
#     def get(self, request, username):
#         try:
#             user = User.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return HttpResponse('User does not exist')
#         month_joined = user.date_joined.strftime('%b, %Y')
#         album = PostImage.objects.filter(post__owner=user).order_by("-post__created_at")
#         post_with_videos = user.post_set.exclude(video__isnull=True).exclude(video__exact='')
#         print(post_with_videos)
#         ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album, 'post_with_vid': post_with_videos}
#         return render(request, 'home/my-profile-videos.html', ctx)

class MediaView(LoginRequiredMixin, View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        album = PostImage.objects.filter(post__owner=user).order_by("-post__created_at")
        ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album}
        return render(request, 'home/my-profile-media.html', ctx)

class AboutView(LoginRequiredMixin, View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        album = PostImage.objects.filter(post__owner=user).order_by("-post__created_at")
        ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album}
        return render(request, 'home/my-profile-about.html', ctx)

class ContactsView(LoginRequiredMixin, View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        album = PostImage.objects.filter(post__owner=user).order_by("-post__created_at")
        ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album}
        return render(request, 'home/my-profile-contacts.html', ctx)

# class EventsView(View):
#     def get(self, request, username):
#         return render(request, 'home/my-profile-events.html')

# class ActivityView(View):
#     def get(self, request, username):
#         return render(request, 'home/my-profile-activity.html')

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddContactView(LoginRequiredMixin, View):
    """
        Adds a new contact
        to a user's contact list
    """
    def post(self, request, username, pk):
        """Creates a new UserContact Object
        """
        if request.user.username != username:
            return HttpResponse('403 Forbidden')

        new_contact = get_object_or_404(User, id=pk)
        usercontact = UserContact(profile=request.user.profile, contact=new_contact)
        try:
            usercontact.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return JsonResponse({"text": new_contact.get_full_name() + ' has been added to your contacts'})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteContactView(LoginRequiredMixin, View):
    """
        Deletes a contact
        from a user's contact list
    """
    def post(self, request, username, pk) :
        """
            Deletes a UserContact object
        """
        #print("Delete PK", pk)
        old_contact = get_object_or_404(User, id=pk)
        try:
            usercontact = UserContact.objects.get(profile=request.user.profile, contact=old_contact).delete()
        except UserContact.DoesNotExist as e:
            pass
        return JsonResponse({"text": old_contact.get_full_name() + ' has been removed from your contacts'})

class EditProfileView(LoginRequiredMixin, View):
    """
        Handles user profile Edit
    """
    def get(self, request, username):
        """
            returns user profile
            edit form
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        return render(request, 'home_modified/edit_profile.html')

    def post(self, request, username):
        """
            Updates user profile
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        if request.user != user:
            return HttpResponse('User not authorized')
        user_profile = user.profile
        if (request.FILES.get("image")):
            image_form = UpdateProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
            if image_form.is_valid():
                image_form.save()
                return render(request, 'home_modified/edit_profile.html')
            else:
                return render(request, 'home_modified/edit_profile.html', {'img_error': image_form.errors})
        elif (request.FILES.get("background_photo")):
            background_photo_form = UpdateProfileBackgroundPhotoForm(request.POST, request.FILES, instance=request.user.profile)
            if background_photo_form.is_valid():
                background_photo_form.save()
                return render(request, 'home_modified/edit_profile.html')
            else:
                return render(request, 'home_modified/edit_profile.html', {'img_error': image_form.errors})
        elif(request.POST.get("username")):
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

            if user_form.is_valid():
                user_form.save()
            else:
                return render(request, 'home_modified/edit_profile.html', {'form_error': user_form.errors})
            if profile_form.is_valid():
                profile_form.save()
            else:
                return render(request, 'home_modified/edit_profile.html', {'form_error': profile_form.errors})
            return HttpResponseRedirect('/' + request.POST.get("username") + '/edit')
        return render(request, 'home_modified/edit_profile.html')

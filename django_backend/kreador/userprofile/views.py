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
from .models import Post, Comment, UserContact, PostImage, PostLike, Poll, PollOption, Voter
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import PostForm, CommentForm, ReplyForm
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
import json
# Create your views here.
class ProfileView(View):
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
        album = PostImage.objects.filter(post__owner=user)[:5]
        #print('album:', album)
        ctx = {'month_joined': month_joined, 'post_list': post_list, 'profile_owner': user, 'album': album}
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
        #print(request.POST)
        #print(request.FILES)
        new_post = Post.objects.create(text=request.POST.get('text'), owner=user)
        new_post.save()
        if request.FILES.getlist('picture[0]'):
            # creates and saves post image
            for key in request.FILES.keys():
                #loops through each uploaded image file
                if key.startswith('picture'):
                    value=request.FILES.getlist(key)[0]
                    new_post_image = PostImage.objects.create(image=value, post=new_post)
                    new_post_image.save()
        elif request.FILES.getlist('video'):
            # saves video file    
            new_post.video = request.FILES.getlist('video')[0]
            new_post.save()
        #post_form = PostForm(request.POST, request.FILES or None)
    
        #if not post_form.is_valid():
        #    return HttpResponse('Invalid form')

        # Add owner to the model before saving
        #saved_form = post_form.save(commit=False)
        #saved_form.owner = user
        #saved_form.save()
        #post_form.save_m2m()
        next = request.POST.get('next', '/home')
        #redirects to the value of next form attribute
        return HttpResponseRedirect(next)

class PollView(View):
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
        polloptions = [request.POST.get('firstoption'), request.POST.get('secondoption'), request.POST.get('thirdoption'), request.POST.get('fourthoption')]
        validpolloptions = []
        for polloption in polloptions:
            if polloption:
                validpolloptions.append(polloption)
        if len(validpolloptions) < 2:
            return HttpResponse('Invalid Poll')
        new_poll = Poll.objects.create(question=request.POST.get('pollquestion'), owner=user)
        new_poll.save()
        for i in range(len(validpolloptions)):
            newpolloption = PollOption.objects.create(text=validpolloptions[i], poll=new_poll, index=i + 1)
            newpolloption.save()
        next = request.POST.get('next', '/home')
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
            return HttpResponse('User not authorized', status-404)
        post_obj.delete()
        return HttpResponse()

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

class PostCommentView(View):
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

class PostReplyView(View):
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

class VideoView(View):
    def get(self, request, username):
        return render(request, 'home/my-profile-videos.html')

class MediaView(View):
    def get(self, request, username):
        return render(request, 'home/my-profile-media.html')

class AboutView(View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)            
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        album = PostImage.objects.filter(post__owner=user)[:5]
        ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album}
        return render(request, 'home/my-profile-about.html', ctx)

class ConnectionsView(View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)            
        except ObjectDoesNotExist:
            return HttpResponse('User does not exist')
        month_joined = user.date_joined.strftime('%b, %Y')
        album = PostImage.objects.filter(post__owner=user)[:5]
        ctx = {'month_joined': month_joined, 'profile_owner': user, 'album': album}
        return render(request, 'home/my-profile-connections.html', ctx)

class EventsView(View):
    def get(self, request, username):
        return render(request, 'home/my-profile-events.html')

class ActivityView(View):
    def get(self, request, username):
        return render(request, 'home/my-profile-activity.html')

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
            return HttpResponse('403 FOrbidden')

        new_contact = get_object_or_404(User, id=pk)
        usercontact = UserContact(profile=request.user.profile, contact=new_contact)
        try:
            usercontact.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()
 
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

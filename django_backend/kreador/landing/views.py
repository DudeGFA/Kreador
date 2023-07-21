"""
    Contains class:
        LandingView
"""
from django.views import View
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
# Create your views here.
class LandingView(View):
    """
        Returns Landing page
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:homepage')
        return render(request, 'home/landing.html')

class UserRegView(View):
    def post(self, request):
        print(request.POST)
        newform = NewUserForm(request.POST)
        #print(newform)
        if newform.is_valid():
            new_user = newform.save()
            login(request, new_user)
            return redirect("home:homepage")
        return render(request, 'home/sign-up.html')

    def get(self, request):
        return render(request, 'home/sign-up.html')
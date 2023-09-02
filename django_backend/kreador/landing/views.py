"""
    Contains class:
        LandingView
"""
from django.views import View
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import json
from django.contrib.auth.views import LoginView, LogoutView
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
        newform = NewUserForm(request.POST)
        if newform.is_valid():
            new_user = newform.save()
            login(request, new_user)
            if not request.POST.get("persistentsession"):
                request.session.set_expiry(0)
            return redirect("/" + new_user.username + '/edit/')
        return render(request, 'home/sign-up.html', {'form_error': newform.errors})

    def get(self, request):
        return render(request, 'home/sign-up.html')

class LoginView(LoginView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if not data.get("persistentsession"):
            request.session.set_expiry(0)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)

class LogoutView(LogoutView):
    pass
# class LoginView(LoginView):
#     def post(self, request):
#         result = super().post(request)
#         data = json.loads(request.body.decode("utf-8"))
#         print(data)
#         #if not data.get("persistentsession"):
#         #    request.session.set_expiry(0)
#         return result
from django.shortcuts import render
from django.views import View

# Create your views here.
class DirectMessage(View):
    def get(self, request):
        return render(request, 'home/messaging.html')
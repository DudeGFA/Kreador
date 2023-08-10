from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .serializers import CommentSerializer, ReplySerializer
from userprofile.models import Comment, Reply
from django.db.models import F
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
      if request.GET.get("postid"):
        self.queryset = Comment.objects.filter(post__id=request.GET.get("postid")).order_by("-created_at")
      return self.list(request, *args, **kwargs)
    
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReplyList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    def get(self, request, *args, **kwargs):
      if request.GET.get("commentid"):
        self.queryset = Reply.objects.filter(comment__id=request.GET.get("commentid")).order_by("-created_at")
      return self.list(request, *args, **kwargs)
    
    def post(self, request, format=None):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
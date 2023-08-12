from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .serializers import CommentSerializer, ReplySerializer, CommentLikeSerializer, ReplyLikeSerializer
from userprofile.models import Comment, Reply, CommentLike, ReplyLike
from django.db.models import F
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from django.http import Http404

class CommentListView(generics.ListCreateAPIView):
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

class CommentLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_object(self, comment_id, **kwargs):
        try:
            return CommentLike.objects.get(comment=comment_id, **kwargs)
        except CommentLike.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        #console.log(request.POST)
        #Data = {"comment": request.POST.get("id")}
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        comment_like = self.get_object(request.data.get("comment"))
        serializer = CommentLikeSerializer(comment_like)
        return Response(serializer.data)

    def delete(self, request,format=None):
        comment_like = self.get_object(request.data.get("comment"), user=request.user)
        serializer = CommentLikeSerializer(comment_like)
        comment_like.delete()
        return Response(serializer.data)

class ReplyLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_object(self, reply_id, **kwargs):
        try:
            return ReplyLike.objects.get(reply=reply_id, **kwargs)
        except ReplyLike.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        #console.log(request.POST)
        #Data = {"comment": request.POST.get("id")}
        serializer = ReplyLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        reply_like = self.get_object(request.data.get("reply"))
        serializer = ReplyLikeSerializer(reply_like)
        return Response(serializer.data)

    def delete(self, request,format=None):
        reply_like = self.get_object(request.data.get("reply"), user=request.user)
        serializer = ReplyLikeSerializer(reply_like)
        reply_like.delete()
        return Response(serializer.data)
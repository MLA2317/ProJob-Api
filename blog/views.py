from django.shortcuts import render
from rest_framework import viewsets, status, serializers, generics, permissions
from .serializer import BodySerializer, BlogDetailSerializer, BlogPostSerializer, CommentSerializer
from .models import Blog, Body, Comment


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogPostSerializer
        return BlogDetailSerializer


class BodyRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Body.objects.all()
    serializer_class = BodySerializer


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(mini_comment_id__isnull=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['blog_id'] = self.kwargs.get('blog_id')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        blog_id = self.kwargs.get('blog_id')
        qs = qs.filter(blog_id=blog_id)
        return qs



from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from .serializer import BodySerializer, BlogDetailSerializer, BlogPostSerializer, CommentSerializer
from .models import Blog, Body, Comment


# class BlogViewSet(viewsets.ModelViewSet):




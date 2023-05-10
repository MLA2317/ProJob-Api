from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializer import ContactSerializer, SubscribeSerializer
from .models import Contact, Subscribe


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SubscribeListCreateView(generics.ListCreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer



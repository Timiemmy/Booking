from django.shortcuts import render
from rest_framework import generics
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

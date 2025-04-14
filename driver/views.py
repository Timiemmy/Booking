from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Driver, DriverVerification
from .serializers import DriverSerializer, DriverVerificationSerializer


class DriverListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
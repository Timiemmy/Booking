from django.shortcuts import render
from django.views import generic
from .models import ComapanyLocation
from .serializers import CompanyLocationSerializer


class CompanyLocationListView(generic.ListView):
    queryset = ComapanyLocation.objects.all()
    serializer_class = CompanyLocationSerializer
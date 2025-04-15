from django.urls import path
from . import views

app_name = 'company_location'

urlpatterns = [
    path('', views.CompanyLocationListView.as_view(), name='companylocation-list'),
]
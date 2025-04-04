from django.urls import path
from . import views

app_name = 'useraccount'

urlpatterns = [
    path('', views.UserView.as_view(), name='user-list'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
]
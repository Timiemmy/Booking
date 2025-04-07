from django.urls import path
from . import views

app_name = 'useraccount'

urlpatterns = [
    path('', views.UserView.as_view(), name='user-list'),
    path('create', views.CreateUserView.as_view(), name='user-create'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),

    path('<int:pk>/address', views.AddressCreateView.as_view(), name='address-create'),
    path('<int:pk>/address/<int:address_pk>', views.AddressDetailView.as_view(), name='address-detail'),
    path('<int:pk>/address/<int:address_pk>/delete', views.AddressDeleteView.as_view(), name='address-delete'),
]
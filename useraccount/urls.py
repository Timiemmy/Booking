from django.urls import path
from . import views


app_name = 'useraccount'

urlpatterns = [
    path('api/', views.UserView.as_view(), name='user-list'),
    path('api/create', views.CreateUserView.as_view(), name='user-create'),
    path('api/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('api/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),

    path('api/<int:pk>/address', views.AddressCreateView.as_view(), name='address-create'),
    path('api/<int:pk>/address/<int:address_pk>', views.AddressDetailView.as_view(), name='address-detail'),
    path('api/<int:pk>/address/<int:address_pk>/delete',
         views.AddressDeleteView.as_view(), name='address-delete'),
]
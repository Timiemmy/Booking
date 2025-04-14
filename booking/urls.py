from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking-list'),
    path('user-bookings/', views.UserBookingListView.as_view(), name='user-booking-list'),
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('<int:pk>/delete/', views.BookingDestroyView.as_view(), name='booking-delete'),
]
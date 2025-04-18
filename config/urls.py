"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from allauth.account.views import ConfirmEmailView
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    re_path(
        "auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(), name="account_confirm_email",),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('users/', include('useraccount.urls', namespace='useraccount')),
    path('vehicles/', include('vehicle.urls', namespace='vehicle')),
    path('drivers/', include('driver.urls', namespace='driver')),
    path('bookings/', include('booking.urls', namespace='booking')),
    path('company/',include('companylocation.urls', namespace='company_location')),
]

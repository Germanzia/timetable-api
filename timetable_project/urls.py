"""
Main URL configuration for timetable_project.

This file routes all incoming requests to the appropriate URL patterns.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    """
    Home page - redirect to dashboard if logged in, otherwise to login page.
    """
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/login/')


urlpatterns = [
    # Home & Admin
    path('', home, name='home'),
    path('admin/', admin.site.urls, name='admin'),

    # User-facing pages (HTML)
    path('dashboard/', include('timetables.dashboard_urls')),
    path('login/', include('timetables.login_urls')),
    path('logout/', include('timetables.logout_urls')),
    path('change-password/', include('timetables.password_urls')),
    # API endpoints (JSON - Admin only access)
    # All endpoints under /api/ are protected by IsAdminUser permission
    path('api/', include('timetables.api_urls')),
]
"""
Logout URL configuration.

Handles user logout and session cleanup.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Custom logout (clears session and redirects to login)
    path('', views.custom_logout, name='logout'),
]
"""
Login URL configuration.

Handles user authentication.
"""

from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login page
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
]
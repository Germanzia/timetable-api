"""
Password change URL configuration.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.change_password_page, name='change_password'),
    path('api/', views.change_password_api, name='change_password_api'),
]
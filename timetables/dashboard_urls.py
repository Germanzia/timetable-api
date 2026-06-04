"""
Dashboard URL configuration.

This is the main user-facing page after login.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard page (Persian performance table)
    path('', views.performance_table_fa, name='dashboard'),
]
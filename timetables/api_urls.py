"""
API URL configuration (JSON endpoints).

All endpoints here are restricted to Admin users only.
Regular users cannot access these endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for all ViewSets
router = DefaultRouter()
router.register(r'contract', views.ContractViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'unit', views.UnitViewSet)
router.register(r'month', views.MonthViewSet)
router.register(r'year', views.YearViewSet)
router.register(r'position', views.PositionViewSet)
router.register(r'staff', views.StaffViewSet)
router.register(r'performance', views.PerformanceViewSet)

urlpatterns = [
    # All API endpoints (protected by IsAdminUser permission in views)
    path('', include(router.urls)),

    # Import endpoint (placeholder - to be implemented)
    path('import/', views.import_performance_page, name='api_import'),
    # Update performance endpoint (for inline editing)
    path('update-performance/', views.update_performance_field, name='update_performance'),
    path('debug-user/', views.debug_user, name='debug_user'),
]
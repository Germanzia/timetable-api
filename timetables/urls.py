"""
URL configuration for timetables app.

This file defines both:
- HTML user-facing pages (dashboard, password change, etc.)
- JSON API endpoints (restricted to admin users)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ============================================================================
# API Router (JSON endpoints - Admin only)
# ============================================================================

router = DefaultRouter()
router.register(r'contract', views.ContractViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'unit', views.UnitViewSet)
router.register(r'month', views.MonthViewSet)
router.register(r'year', views.YearViewSet)
router.register(r'position', views.PositionViewSet)
router.register(r'staff', views.StaffViewSet)
router.register(r'performance', views.PerformanceViewSet)

# ============================================================================
# URL Patterns
# ============================================================================

urlpatterns = [
    # API Root (JSON) - Shows all available endpoints
    path('', views.api_root, name='api-root'),

    # HTML Pages (User-facing)
    path('performance-table/', views.performance_table, name='performance_table'),
    path('performance-table-fa/', views.performance_table_fa, name='performance_table_fa'),
    path('change-password/', views.change_password_page, name='change_password'),
    path('change-password-api/', views.change_password_api, name='change_password_api'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('import-performance/', views.import_performance_page, name='import_performance'),
    path('update-performance/', views.update_performance_field, name='update_performance'),
    path('debug-user/', views.debug_user, name='debug_user'),
    # Include all API router endpoints
    path('', include(router.urls)),
]
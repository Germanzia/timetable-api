from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

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
    path('', views.api_root, name='api-root'),
    path('performance-table/', views.performance_table, name='performance_table'),
    path('', include(router.urls)),
]
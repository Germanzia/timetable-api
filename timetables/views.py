from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import (
    Contract, Status, Unit, Month, Year,
    Position, Staff, Performance
)
from .serializers import (
    ContractSerializer, StatusSerializer, UnitSerializer,
    MonthSerializer, YearSerializer, PositionSerializer,
    StaffSerializer, PerformanceSerializer
)
from .permissions import (
    IsAdmin, IsOfficeManager, IsHeadOfUnit, IsRegularStaff, CanViewStaffList
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    """Custom API root with all endpoints"""
    return Response({
        'api_endpoints': {
            'contracts': request.build_absolute_uri(reverse('contract-list')),
            'statuses': request.build_absolute_uri(reverse('status-list')),
            'units': request.build_absolute_uri(reverse('unit-list')),
            'months': request.build_absolute_uri(reverse('month-list')),
            'years': request.build_absolute_uri(reverse('year-list')),
            'positions': request.build_absolute_uri(reverse('position-list')),
            'staff': request.build_absolute_uri(reverse('staff-list')),
            'performance': request.build_absolute_uri(reverse('performance-list')),
        },
        'html_pages': {
            'performance_table': request.build_absolute_uri(reverse('performance_table')),
        }
    })
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('contract_id')
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by('status_id')
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('unit_id')
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all().order_by('month_id')
    serializer_class = MonthSerializer
    permission_classes = [IsAuthenticated]


class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all().order_by('year_id')
    serializer_class = YearSerializer
    permission_classes = [IsAuthenticated]


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('position_id')
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, CanViewStaffList]
    queryset = Staff.objects.none()  # Placeholder

    def get_queryset(self):
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)

            if staff.position_id == 1:  # Admin
                return Staff.objects.all().order_by('staff_id')
            elif staff.position_id == 2:  # Office Manager
                return Staff.objects.all().order_by('staff_id')
            elif staff.position_id == 3:  # Head of Unit
                return Staff.objects.filter(unit_id=staff.unit_id).order_by('staff_id')
            else:
                return Staff.objects.none()
        except Staff.DoesNotExist:
            return Staff.objects.none()


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Performance.objects.none()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff_id', 'year_id', 'month_id']
    search_fields = ['staff__staff_name_eng', 'staff__staff_family_eng']

    def get_queryset(self):
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)

            if staff.position_id == 1:  # Admin
                return Performance.objects.all().order_by('-performance_id')
            elif staff.position_id == 2:  # Office Manager
                return Performance.objects.all().order_by('-performance_id')
            elif staff.position_id == 3:  # Head of Unit
                unit_staff_ids = Staff.objects.filter(unit_id=staff.unit_id).values_list('staff_id', flat=True)
                return Performance.objects.filter(staff_id__in=unit_staff_ids).order_by('-performance_id')
            elif staff.position_id == 4:  # Regular Staff
                return Performance.objects.filter(staff_id=staff.staff_id).order_by('-performance_id')
        except Staff.DoesNotExist:
            return Performance.objects.none()

    def update(self, request, *args, **kwargs):
        performance = self.get_object()
        user = request.user
        staff = Staff.objects.get(user=user)

        if staff.position_id == 1:  # Admin
            return super().update(request, *args, **kwargs)

        if staff.position_id == 2:  # Office Manager
            allowed_fields = [
                'performance_approved_hourly_leave',
                'performance_approved_overtime',
                'performance_approved_compensatory_timeoff'
            ]
            filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
            request._full_data = filtered_data
            return super().update(request, *args, **kwargs)

        if staff.position_id == 3:  # Head of Unit
            if performance.staff.unit_id != staff.unit_id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only edit performance for your unit")

            allowed_fields = [
                'performance_proposed_overtime',
                'performance_proposed_compensatory_timeoff'
            ]
            filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
            request._full_data = filtered_data
            return super().update(request, *args, **kwargs)

        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("You do not have permission to edit")

    def destroy(self, request, *args, **kwargs):
        user = request.user
        staff = Staff.objects.get(user=user)

        if staff.position_id != 1:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only Administrator can delete records")

        return super().destroy(request, *args, **kwargs)


def performance_table(request):
    """HTML table view for performance records"""

    # Get all performance records with related data
    performances = Performance.objects.select_related(
        'staff', 'staff__unit', 'staff__position', 'year', 'month'
    ).all().order_by('-performance_id')

    # Apply filters
    staff_id = request.GET.get('staff')
    year_id = request.GET.get('year')
    month_id = request.GET.get('month')

    if staff_id:
        performances = performances.filter(staff_id=staff_id)
    if year_id:
        performances = performances.filter(year_id=year_id)
    if month_id:
        performances = performances.filter(month_id=month_id)

    # Pagination (50 records per page)
    paginator = Paginator(performances, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'performances': page_obj,
        'staff_list': Staff.objects.all().order_by('staff_name_eng'),
        'year_list': Year.objects.all().order_by('-year_number'),
        'month_list': Month.objects.all().order_by('month_id'),
        'selected_staff': staff_id,
        'selected_year': year_id,
        'selected_month': month_id,
    }

    return render(request, 'performance_table.html', context)
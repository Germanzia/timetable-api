"""
Views for timetables app.

This file contains:
- API Views (JSON endpoints - Admin only)
- HTML Views (User-facing pages)
- AJAX endpoints (Inline editing, password change)
"""

import json
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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
    IsAdmin, IsOfficeManager, IsHeadOfUnit, IsRegularStaff,
    CanViewStaffList, IsAdminUser
)


# ============================================================================
# API Views (JSON endpoints - Admin only)
# ============================================================================

class ContractViewSet(viewsets.ModelViewSet):
    """Contract API endpoint - Admin only."""
    queryset = Contract.objects.all().order_by('contract_id')
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class StatusViewSet(viewsets.ModelViewSet):
    """Status API endpoint - Admin only."""
    queryset = Status.objects.all().order_by('status_id')
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UnitViewSet(viewsets.ModelViewSet):
    """Unit API endpoint - Admin only."""
    queryset = Unit.objects.all().order_by('unit_id')
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class MonthViewSet(viewsets.ModelViewSet):
    """Month API endpoint - Admin only."""
    queryset = Month.objects.all().order_by('month_id')
    serializer_class = MonthSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class YearViewSet(viewsets.ModelViewSet):
    """Year API endpoint - Admin only."""
    queryset = Year.objects.all().order_by('year_id')
    serializer_class = YearSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PositionViewSet(viewsets.ModelViewSet):
    """Position API endpoint - Admin only."""
    queryset = Position.objects.all().order_by('position_id')
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class StaffViewSet(viewsets.ModelViewSet):
    """Staff API endpoint - Admin only."""
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Staff.objects.none()

    def get_queryset(self):
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)
            if staff.position_id == 1:
                return Staff.objects.all().order_by('staff_id')
            elif staff.position_id == 2:
                return Staff.objects.all().order_by('staff_id')
            elif staff.position_id == 3:
                return Staff.objects.filter(unit_id=staff.unit_id).order_by('staff_id')
            else:
                return Staff.objects.none()
        except Staff.DoesNotExist:
            return Staff.objects.none()


class PerformanceViewSet(viewsets.ModelViewSet):
    """Performance API endpoint - Admin only."""
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Performance.objects.none()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff_id', 'year_id', 'month_id']
    search_fields = ['staff__staff_name_eng', 'staff__staff_family_eng']

    def get_queryset(self):
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)
            if staff.position_id == 1:
                return Performance.objects.all().order_by('-performance_id')
            elif staff.position_id == 2:
                return Performance.objects.all().order_by('-performance_id')
            elif staff.position_id == 3:
                unit_staff_ids = Staff.objects.filter(unit_id=staff.unit_id).values_list('staff_id', flat=True)
                return Performance.objects.filter(staff_id__in=unit_staff_ids).order_by('-performance_id')
            elif staff.position_id == 4:
                return Performance.objects.filter(staff_id=staff.staff_id).order_by('-performance_id')
        except Staff.DoesNotExist:
            return Performance.objects.none()

    def update(self, request, *args, **kwargs):
        performance = self.get_object()
        user = request.user
        staff = Staff.objects.get(user=user)

        if staff.position_id == 1:
            return super().update(request, *args, **kwargs)

        if staff.position_id == 2:
            allowed_fields = [
                'performance_approved_hourly_leave',
                'performance_approved_overtime',
                'performance_approved_compensatory_timeoff'
            ]
            filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
            request._full_data = filtered_data
            return super().update(request, *args, **kwargs)

        if staff.position_id == 3:
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def api_root(request):
    """API root endpoint showing all available endpoints - Admin only."""
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
            'performance_table_fa': request.build_absolute_uri(reverse('performance_table_fa')),
        }
    })


# ============================================================================
# AJAX Endpoints (Inline editing, password change)
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def update_performance_field(request):
    """AJAX endpoint for updating performance fields"""

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        current_staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff record not found'}, status=403)

    data = json.loads(request.body)
    performance_id = data.get('performance_id')
    field_name = data.get('field_name')
    new_value = data.get('new_value')

    # Define allowed fields per role
    allowed_fields = {
        1: [  # Admin
            'performance_working_days',
            'performance_hourly_overtime',
            'performance_hourly_leave',
            'performance_hourly_absence',
            'performance_daily_absence',
            'performance_annual_leave',
            'performance_sick_leave',
            'performance_daily_reward_leave',
            'performance_daily_mission'
        ],
        2: [  # Office Manager
            'performance_approved_hourly_leave',
            'performance_approved_overtime',
            'performance_approved_compensatory_timeoff'
        ],
        3: [  # Head of Unit
            'performance_proposed_overtime',
            'performance_proposed_compensatory_timeoff'
        ]
    }

    # Debug logging
    print(f"User: {request.user.username}")
    print(f"Position ID: {current_staff.position_id}")
    print(f"Field name: {field_name}")
    print(f"Allowed for position: {allowed_fields.get(current_staff.position_id, [])}")

    if current_staff.position_id not in allowed_fields:
        return JsonResponse({'error': f'Permission denied. Your position ID is {current_staff.position_id}'},
                            status=403)

    if field_name not in allowed_fields[current_staff.position_id]:
        return JsonResponse({'error': f'You are not allowed to edit this field: {field_name}'}, status=403)

    try:
        performance = Performance.objects.get(performance_id=performance_id)

        # For Head of Unit, verify they belong to same unit
        if current_staff.position_id == 3:
            if performance.staff.unit_id != current_staff.unit_id:
                return JsonResponse({'error': 'You can only edit records for your unit'}, status=403)

        # Update the field
        if new_value == '' or new_value is None:
            setattr(performance, field_name, None)
        else:
            setattr(performance, field_name, new_value)

        performance.save()

        return JsonResponse({
            'success': True,
            'message': 'Updated successfully',
            'new_value': new_value
        })

    except Performance.DoesNotExist:
        return JsonResponse({'error': 'Performance record not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def change_password_api(request):
    """API endpoint for changing user password."""

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not request.user.check_password(old_password):
            return JsonResponse({'error': 'Wrong password'}, status=400)

        if not new_password or len(new_password) < 4:
            return JsonResponse({'error': 'Password must be at least 4 characters'}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        return JsonResponse({'success': True, 'message': 'Password changed successfully'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# HTML Views (User-facing pages)
# ============================================================================

def performance_table(request):
    """English HTML table view - redirects to Persian version."""
    return redirect('performance_table_fa')


def performance_table_fa(request):
    """Persian/RTL HTML table view with role-based permissions."""

    if not request.user.is_authenticated:
        return redirect('/login/?next=' + request.path)

    try:
        current_staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        return render(request, 'performance_table_fa.html', {
            'performances': [],
            'unit_list': [],
            'staff_list': [],
            'all_staff_list': [],
            'year_list': Year.objects.all().order_by('-year_number'),
            'month_list': Month.objects.all().order_by('month_id'),
            'selected_unit': None,
            'selected_staff': None,
            'selected_year': None,
            'selected_month': None,
            'user_position': 0,
            'user_name': 'کاربر',
            'error_message': 'شما دسترسی به این صفحه ندارید'
        })

    position_id = current_staff.position_id

    # Base queryset
    performances = Performance.objects.select_related(
        'staff', 'staff__unit', 'staff__position', 'year', 'month'
    )

    # Apply role-based permissions
    if position_id == 1 or position_id == 2:
        performances = performances.all()
        staff_list = Staff.objects.all()
        unit_list = Unit.objects.all()
    elif position_id == 3:
        performances = performances.filter(staff__unit_id=current_staff.unit_id)
        staff_list = Staff.objects.filter(unit_id=current_staff.unit_id)
        unit_list = Unit.objects.filter(unit_id=current_staff.unit_id)
    elif position_id == 4:
        performances = performances.filter(staff_id=current_staff.staff_id)
        staff_list = Staff.objects.filter(staff_id=current_staff.staff_id)
        unit_list = Unit.objects.filter(unit_id=current_staff.unit_id)
    else:
        performances = performances.none()
        staff_list = Staff.objects.none()
        unit_list = Unit.objects.none()

    # Apply filters
    unit_id = request.GET.get('unit')
    staff_id = request.GET.get('staff')
    year_id = request.GET.get('year')
    month_id = request.GET.get('month')

    if position_id == 3 and unit_id:
        if int(unit_id) != current_staff.unit_id:
            unit_id = None
    if position_id == 4 and staff_id:
        if int(staff_id) != current_staff.staff_id:
            staff_id = None

    if unit_id:
        performances = performances.filter(staff__unit_id=unit_id)
    if staff_id:
        performances = performances.filter(staff_id=staff_id)
    if year_id:
        performances = performances.filter(year_id=year_id)
    if month_id:
        performances = performances.filter(month_id=month_id)

    # Pagination
    paginator = Paginator(performances, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'performances': page_obj,
        'unit_list': unit_list.order_by('unit_name_fa') if hasattr(unit_list, 'order_by') else unit_list,
        'staff_list': staff_list.order_by('staff_name_fa') if hasattr(staff_list, 'order_by') else staff_list,
        'all_staff_list': Staff.objects.all().order_by('staff_name_fa'),
        'year_list': Year.objects.all().order_by('-year_number'),
        'month_list': Month.objects.all().order_by('month_id'),
        'selected_unit': unit_id,
        'selected_staff': staff_id,
        'selected_year': year_id,
        'selected_month': month_id,
        'user_position': position_id,
        'user_name': f'{current_staff.staff_name_fa} {current_staff.staff_family_fa}',
    }

    return render(request, 'performance_table_fa.html', context)


def change_password_page(request):
    """Password change page."""

    if not request.user.is_authenticated:
        return redirect('/login/?next=' + request.path)

    try:
        current_staff = Staff.objects.get(user=request.user)
        user_name = f'{current_staff.staff_name_fa} {current_staff.staff_family_fa}'
    except Staff.DoesNotExist:
        user_name = request.user.username

    return render(request, 'change_password.html', {'user_name': user_name})


def custom_logout(request):
    """Custom logout view that clears the session."""
    logout(request)
    return redirect('/login/')


def import_performance_page(request):
    """Import page for Excel upload - Admin only."""

    if not request.user.is_authenticated:
        return redirect('/login/?next=' + request.path)

    try:
        current_staff = Staff.objects.get(user=request.user)
        if current_staff.position_id != 1:
            return redirect('/dashboard/')
        user_name = f'{current_staff.staff_name_fa} {current_staff.staff_family_fa}'
    except Staff.DoesNotExist:
        return redirect('/login/')

    return render(request, 'import_performance.html', {
        'user_name': user_name,
        'user_position': 1,
    })


def debug_user(request):
    """Debug endpoint to check user position"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'})

    try:
        staff = Staff.objects.get(user=request.user)
        return JsonResponse({
            'username': request.user.username,
            'staff_id': staff.staff_id,
            'position_id': staff.position_id,
            'position_name': staff.position.position_name_eng if staff.position else 'None'
        })
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'})


def debug_user(request):
    """Debug endpoint to check user position"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'})

    try:
        staff = Staff.objects.get(user=request.user)
        return JsonResponse({
            'username': request.user.username,
            'staff_id': staff.staff_id,
            'position_id': staff.position_id,
            'position_name': staff.position.position_name_eng if staff.position else 'None'
        })
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'})
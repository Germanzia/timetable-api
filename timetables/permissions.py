from rest_framework import permissions
from .models import Staff, Position


class IsAdmin(permissions.BasePermission):
    """Administrator - Full access"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 1  # Administrator
        except Staff.DoesNotExist:
            return request.user.is_superuser


class IsOfficeManager(permissions.BasePermission):
    """Office Manager - Can edit approved fields"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 2  # Office Manager
        except Staff.DoesNotExist:
            return False


class IsHeadOfUnit(permissions.BasePermission):
    """Head of Unit - Can edit proposed fields for their unit"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 3  # Head of Unit
        except Staff.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Check if the performance record belongs to staff in their unit
        try:
            staff = Staff.objects.get(user=request.user)
            return obj.staff.unit_id == staff.unit_id
        except:
            return False


class IsRegularStaff(permissions.BasePermission):
    """Regular Staff - Can only view their own performance"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 4  # Regular Staff
        except Staff.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Check if the performance record belongs to this staff member
        try:
            staff = Staff.objects.get(user=request.user)
            return obj.staff_id == staff.staff_id
        except:
            return False


class CanViewStaffList(permissions.BasePermission):
    """Who can see the staff list"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            # Admin, Office Manager, Head of Unit can see staff list
            return staff.position_id in [1, 2, 3]
        except Staff.DoesNotExist:
            return False
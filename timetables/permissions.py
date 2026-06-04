"""
Custom permission classes for role-based access control.

Position IDs:
- 1: Administrator (full access)
- 2: Office Manager (can edit approved fields)
- 3: Head of Unit (can edit proposed fields for their unit)
- 4: Regular Staff (view only)
"""

from rest_framework import permissions
from .models import Staff


class IsAdmin(permissions.BasePermission):
    """Administrator - Full access to everything."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 1
        except Staff.DoesNotExist:
            return request.user.is_superuser


class IsOfficeManager(permissions.BasePermission):
    """Office Manager - Can edit approved fields (green cells)."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 2
        except Staff.DoesNotExist:
            return False


class IsHeadOfUnit(permissions.BasePermission):
    """Head of Unit - Can edit proposed fields (yellow cells) for their unit."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 3
        except Staff.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """Check if the performance record belongs to staff in their unit."""
        try:
            staff = Staff.objects.get(user=request.user)
            return obj.staff.unit_id == staff.unit_id
        except:
            return False


class IsRegularStaff(permissions.BasePermission):
    """Regular Staff - Can only view their own performance records."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 4
        except Staff.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """Check if the performance record belongs to this staff member."""
        try:
            staff = Staff.objects.get(user=request.user)
            return obj.staff_id == staff.staff_id
        except:
            return False


class CanViewStaffList(permissions.BasePermission):
    """
    Who can see the staff list.
    Allowed: Administrator, Office Manager, Head of Unit.
    Denied: Regular Staff.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id in [1, 2, 3]
        except Staff.DoesNotExist:
            return False


class IsAdminUser(permissions.BasePermission):
    """
    JSON API access - Restricted to Administrator only.
    Used to protect JSON endpoints from non-admin users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            staff = Staff.objects.get(user=request.user)
            return staff.position_id == 1
        except Staff.DoesNotExist:
            return request.user.is_superuser
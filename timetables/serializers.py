"""
Serializers for converting model instances to JSON and validating input data.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Contract, Status, Unit, Month, Year,
    Position, Staff, Performance
)


# ============================================================================
# Lookup Table Serializers
# ============================================================================

class ContractSerializer(serializers.ModelSerializer):
    """Serializer for Contract model."""

    class Meta:
        model = Contract
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for Status model."""

    class Meta:
        model = Status
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model."""

    class Meta:
        model = Unit
        fields = '__all__'


class MonthSerializer(serializers.ModelSerializer):
    """Serializer for Month model."""

    class Meta:
        model = Month
        fields = '__all__'


class YearSerializer(serializers.ModelSerializer):
    """Serializer for Year model."""

    class Meta:
        model = Year
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for Position model."""

    class Meta:
        model = Position
        fields = '__all__'


# ============================================================================
# Staff Serializer
# ============================================================================

class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model with human-readable related field names."""

    # Human-readable names from related tables
    position_name = serializers.CharField(
        source='position.position_name_eng',
        read_only=True
    )
    unit_name = serializers.CharField(
        source='unit.unit_name_eng',
        read_only=True
    )
    contract_name = serializers.CharField(
        source='contract.contract_name_eng',
        read_only=True
    )
    status_name = serializers.CharField(
        source='status.status_name_eng',
        read_only=True
    )
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Staff
        fields = [
            'staff_id',
            'staff_name_eng',
            'staff_family_eng',
            'staff_name_fa',
            'staff_family_fa',
            'staff_code',
            'position_id',
            'position_name',
            'unit_id',
            'unit_name',
            'contract_id',
            'contract_name',
            'status_id',
            'status_name',
            'user_id',
            'username',
        ]


# ============================================================================
# Performance Serializer
# ============================================================================

class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance model with human-readable related field names."""

    # Staff information
    staff_name = serializers.CharField(
        source='staff.staff_name_eng',
        read_only=True
    )
    staff_family = serializers.CharField(
        source='staff.staff_family_eng',
        read_only=True
    )
    full_name = serializers.SerializerMethodField()

    # Time period information
    year_number = serializers.IntegerField(
        source='year.year_number',
        read_only=True
    )
    month_name = serializers.CharField(
        source='month.month_name',
        read_only=True
    )

    # Related information from staff
    unit_name = serializers.CharField(
        source='staff.unit.unit_name_eng',
        read_only=True
    )
    position_name = serializers.CharField(
        source='staff.position.position_name_eng',
        read_only=True
    )

    class Meta:
        model = Performance
        fields = [
            'performance_id',
            'staff_id',
            'full_name',
            'staff_name',
            'staff_family',
            'unit_name',
            'position_name',
            'year_id',
            'year_number',
            'month_id',
            'month_name',
            'performance_working_days',
            'performance_hourly_overtime',
            'performance_hourly_leave',
            'performance_hourly_absence',
            'performance_daily_absence',
            'performance_annual_leave',
            'performance_sick_leave',
            'performance_daily_reward_leave',
            'performance_daily_mission',
            'performance_proposed_overtime',
            'performance_proposed_compensatory_timeoff',
            'performance_approved_hourly_leave',
            'performance_approved_overtime',
            'performance_approved_compensatory_timeoff',
        ]

    def get_full_name(self, obj):
        """Return full name as 'First Last' format."""
        if obj.staff:
            return f"{obj.staff.staff_name_eng} {obj.staff.staff_family_eng}".strip()
        return None


# ============================================================================
# User Serializer
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's built-in User model."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
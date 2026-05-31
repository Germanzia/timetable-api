from rest_framework import serializers
from .models import (
    Contract, Status, Unit, Month, Year,
    Position, Staff, Performance
)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.position_name_eng', read_only=True)
    unit_name = serializers.CharField(source='unit.unit_name_eng', read_only=True)
    contract_name = serializers.CharField(source='contract.contract_name_eng', read_only=True)
    status_name = serializers.CharField(source='status.status_name_eng', read_only=True)

    class Meta:
        model = Staff
        fields = ['staff_id', 'staff_name_eng', 'staff_family_eng',
                  'staff_name_fa', 'staff_family_fa', 'staff_code',
                  'position_id', 'position_name',
                  'unit_id', 'unit_name',
                  'contract_id', 'contract_name',
                  'status_id', 'status_name']


class PerformanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.staff_name_eng', read_only=True)
    staff_family = serializers.CharField(source='staff.staff_family_eng', read_only=True)
    year_number = serializers.IntegerField(source='year.year_number', read_only=True)
    month_name = serializers.CharField(source='month.month_name', read_only=True)

    class Meta:
        model = Performance
        fields = '__all__'
from rest_framework import viewsets
from .models import (
    Contract, Status, Unit, Month, Year,
    Position, Staff, Performance
)
from .serializers import (
    ContractSerializer, StatusSerializer, UnitSerializer,
    MonthSerializer, YearSerializer, PositionSerializer,
    StaffSerializer, PerformanceSerializer
)

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('contract_id')
    serializer_class = ContractSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by('status_id')
    serializer_class = StatusSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('unit_id')
    serializer_class = UnitSerializer

class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all().order_by('month_id')
    serializer_class = MonthSerializer

class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all().order_by('year_id')
    serializer_class = YearSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('position_id')
    serializer_class = PositionSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by('staff_id')
    serializer_class = StaffSerializer

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().order_by('-performance_id')
    serializer_class = PerformanceSerializer
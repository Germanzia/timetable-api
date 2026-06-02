from django.contrib.auth.models import User
from django.db import models


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    contract_name_fa = models.TextField(blank=True, null=True)
    contract_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract'


class Month(models.Model):
    month_id = models.AutoField(primary_key=True)
    month_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'month'


class Performance(models.Model):
    performance_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    year = models.ForeignKey('Year', models.DO_NOTHING, blank=True, null=True)
    month = models.ForeignKey(Month, models.DO_NOTHING, blank=True, null=True)
    performance_working_days = models.IntegerField(blank=True, null=True)
    performance_hourly_overtime = models.TextField(blank=True, null=True)
    performance_hourly_leave = models.TextField(blank=True, null=True)
    performance_hourly_absence = models.TextField(blank=True, null=True)
    performance_daily_absence = models.IntegerField(blank=True, null=True)
    performance_annual_leave = models.IntegerField(blank=True, null=True)
    performance_sick_leave = models.IntegerField(blank=True, null=True)
    performance_daily_reward_leave = models.IntegerField(blank=True, null=True)
    performance_daily_mission = models.IntegerField(blank=True, null=True)
    performance_proposed_overtime = models.IntegerField(blank=True, null=True)
    performance_proposed_compensatory_timeoff = models.IntegerField(blank=True, null=True)
    performance_approved_hourly_leave = models.TextField(blank=True, null=True)
    performance_approved_overtime = models.IntegerField(blank=True, null=True)
    performance_approved_compensatory_timeoff = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'performance'


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name_fa = models.TextField(blank=True, null=True)
    position_name_eng = models.TextField(blank=True, null=True)
    position_can_login = models.BooleanField(blank=True, null=True)
    position_can_see_own_unit = models.BooleanField(blank=True, null=True)
    position_can_see_all_staff = models.BooleanField(blank=True, null=True)
    position_is_superuser = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff_name_fa = models.TextField(blank=True, null=True)
    staff_family_fa = models.TextField(blank=True, null=True)
    staff_name_eng = models.TextField(blank=True, null=True)
    staff_family_eng = models.TextField(blank=True, null=True)
    staff_code = models.IntegerField(blank=True, null=True)
    contract = models.ForeignKey(Contract, models.DO_NOTHING, blank=True, null=True)
    unit = models.ForeignKey('Unit', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    position = models.ForeignKey(Position, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name_fa = models.TextField(blank=True, null=True)
    status_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_name_fa = models.TextField(blank=True, null=True)
    unit_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'


class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'year'

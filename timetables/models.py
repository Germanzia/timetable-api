"""
Database models for the timetables app.

These models map to existing database tables (managed = False).
The tables are created and maintained externally (via SQL or imports).
"""

from django.contrib.auth.models import User
from django.db import models


# ============================================================================
# Lookup Tables
# ============================================================================

class Contract(models.Model):
    """Contract type lookup table."""

    contract_id = models.AutoField(primary_key=True)
    contract_name_fa = models.TextField(blank=True, null=True)
    contract_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

    def __str__(self):
        return self.contract_name_eng or str(self.contract_id)


class Status(models.Model):
    """Status lookup table (e.g., Active, Inactive, Terminated)."""

    status_id = models.AutoField(primary_key=True)
    status_name_fa = models.TextField(blank=True, null=True)
    status_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.status_name_eng or str(self.status_id)


class Unit(models.Model):
    """Department/Unit lookup table."""

    unit_id = models.AutoField(primary_key=True)
    unit_name_fa = models.TextField(blank=True, null=True)
    unit_name_eng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.unit_name_eng or str(self.unit_id)


class Month(models.Model):
    """Month lookup table."""

    month_id = models.AutoField(primary_key=True)
    month_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'month'
        verbose_name = 'Month'
        verbose_name_plural = 'Months'

    def __str__(self):
        return self.month_name or str(self.month_id)


class Year(models.Model):
    """Year lookup table."""

    year_id = models.AutoField(primary_key=True)
    year_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'year'
        verbose_name = 'Year'
        verbose_name_plural = 'Years'

    def __str__(self):
        return str(self.year_number) if self.year_number else str(self.year_id)


class Position(models.Model):
    """
    Employee position/role lookup table.

    Position IDs:
    - 1: Administrator (full access)
    - 2: Office Manager (edit approved fields)
    - 3: Head of Unit (edit proposed fields)
    - 4: Regular Staff (view only)
    """

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
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.position_name_eng or str(self.position_id)


# ============================================================================
# Core Tables
# ============================================================================

class Staff(models.Model):
    """Staff/Employee information table."""

    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Linked Django user account (for login access)"
    )
    staff_name_fa = models.TextField(blank=True, null=True)
    staff_family_fa = models.TextField(blank=True, null=True)
    staff_name_eng = models.TextField(blank=True, null=True)
    staff_family_eng = models.TextField(blank=True, null=True)
    staff_code = models.IntegerField(blank=True, null=True)

    # Foreign keys
    contract = models.ForeignKey(
        Contract,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    unit = models.ForeignKey(
        Unit,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    position = models.ForeignKey(
        Position,
        models.DO_NOTHING,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        ordering = ['staff_name_eng', 'staff_family_eng']

    def __str__(self):
        if self.staff_name_eng and self.staff_family_eng:
            return f"{self.staff_name_eng} {self.staff_family_eng}"
        return f"Staff {self.staff_id}"

    @property
    def full_name_fa(self):
        """Return full name in Persian."""
        if self.staff_name_fa and self.staff_family_fa:
            return f"{self.staff_name_fa} {self.staff_family_fa}"
        return None

    @property
    def full_name_eng(self):
        """Return full name in English."""
        if self.staff_name_eng and self.staff_family_eng:
            return f"{self.staff_name_eng} {self.staff_family_eng}"
        return None


class Performance(models.Model):
    """
    Monthly performance records for staff.

    Field groups:
    - Working days & hours (first 12 fields from Excel)
    - Proposed fields (editable by Head of Unit)
    - Approved fields (editable by Office Manager)
    """

    performance_id = models.AutoField(primary_key=True)

    # Foreign keys
    staff = models.ForeignKey(
        Staff,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    year = models.ForeignKey(
        Year,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    month = models.ForeignKey(
        Month,
        models.DO_NOTHING,
        blank=True,
        null=True
    )

    # Working days and hours (from Excel import)
    performance_working_days = models.IntegerField(blank=True, null=True)
    performance_hourly_overtime = models.TextField(blank=True, null=True)
    performance_hourly_leave = models.TextField(blank=True, null=True)
    performance_hourly_absence = models.TextField(blank=True, null=True)
    performance_daily_absence = models.IntegerField(blank=True, null=True)
    performance_annual_leave = models.IntegerField(blank=True, null=True)
    performance_sick_leave = models.IntegerField(blank=True, null=True)
    performance_daily_reward_leave = models.IntegerField(blank=True, null=True)
    performance_daily_mission = models.IntegerField(blank=True, null=True)

    # Proposed fields (editable by Head of Unit - yellow cells)
    performance_proposed_overtime = models.IntegerField(blank=True, null=True)
    performance_proposed_compensatory_timeoff = models.IntegerField(blank=True, null=True)

    # Approved fields (editable by Office Manager - green cells)
    performance_approved_hourly_leave = models.TextField(blank=True, null=True)
    performance_approved_overtime = models.IntegerField(blank=True, null=True)
    performance_approved_compensatory_timeoff = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'performance'
        verbose_name = 'Performance'
        verbose_name_plural = 'Performance'
        ordering = ['-performance_id']

    def __str__(self):
        staff_name = str(self.staff) if self.staff else "Unknown"
        return f"Performance {self.performance_id} - {staff_name}"
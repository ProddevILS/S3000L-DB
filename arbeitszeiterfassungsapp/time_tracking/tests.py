from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from arbeitszeiterfassungsapp.accounts.models import Employee
from arbeitszeiterfassungsapp.customers.models import Customer
from arbeitszeiterfassungsapp.projects.models import ActivityType, Project, ProjectActivityRate
from .models import TimeEntry, TimeEntryAuditLog
from .services import audit_changes, start_entry, stop_entry
class TimeTrackingTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('u','u@example.com','pw'); self.emp=Employee.objects.create(user=self.user,display_name='User')
        self.customer=Customer.objects.create(name='Kunde',short_name='K')
        self.dev=ActivityType.objects.create(name='Entwicklung',default_hourly_rate=Decimal('80'),billable_default=True)
        self.pause=ActivityType.objects.create(name='Pause',billable_default=False)
        self.travel=ActivityType.objects.create(name='Fahrzeit',default_hourly_rate=Decimal('50'))
        self.project=Project.objects.create(customer=self.customer,name='Projekt',short_name='P',default_hourly_rate=Decimal('100'),travel_hourly_rate=Decimal('60'))
    def test_start_stop_entry(self):
        e=start_entry(self.emp,self.customer,self.project,self.dev); self.assertEqual(e.status,'running')
        stop_entry(e); e.refresh_from_db(); self.assertEqual(e.status,'completed')
    def test_pause_entry(self):
        e=start_entry(self.emp,self.customer,self.project,self.pause,is_pause=True); stop_entry(e); e.refresh_from_db(); self.assertTrue(e.is_pause); self.assertEqual(e.amount_net,0)
    def test_project_switch_stops_old(self):
        first=start_entry(self.emp,self.customer,self.project,self.dev)
        second=start_entry(self.emp,self.customer,self.project,self.dev,description='neu')
        first.refresh_from_db(); self.assertEqual(first.status,'completed'); self.assertEqual(second.status,'running')
    def test_manual_duration_calculation(self):
        start=timezone.now()-timedelta(hours=2); e=TimeEntry.objects.create(employee=self.emp,customer=self.customer,project=self.project,activity_type=self.dev,start_datetime=start,end_datetime=start+timedelta(minutes=90),status='completed',source='manual')
        self.assertEqual(e.duration_minutes,90); self.assertEqual(e.amount_net,Decimal('150.00'))
    def test_hourly_rate_priority(self):
        ProjectActivityRate.objects.create(project=self.project,activity_type=self.dev,hourly_rate=Decimal('110'))
        e=TimeEntry(employee=self.emp,customer=self.customer,project=self.project,activity_type=self.dev,start_datetime=timezone.now(),end_datetime=timezone.now()+timedelta(hours=1),status='completed')
        self.assertEqual(e.resolve_hourly_rate(),Decimal('110'))
        e.hourly_rate=Decimal('120'); self.assertEqual(e.resolve_hourly_rate(),Decimal('120'))
        t=TimeEntry(employee=self.emp,customer=self.customer,project=self.project,activity_type=self.travel,start_datetime=timezone.now(),end_datetime=timezone.now()+timedelta(hours=1)); self.assertEqual(t.resolve_hourly_rate(),Decimal('60'))
    def test_audit_log(self):
        e=TimeEntry.objects.create(employee=self.emp,customer=self.customer,project=self.project,activity_type=self.dev,start_datetime=timezone.now(),end_datetime=timezone.now()+timedelta(hours=1),description='alt',status='completed')
        old=TimeEntry.objects.get(pk=e.pk); e.description='neu'; e.save(); audit_changes(e,old,self.user,'Korrektur')
        self.assertTrue(TimeEntryAuditLog.objects.filter(time_entry=e,field_name='description').exists())

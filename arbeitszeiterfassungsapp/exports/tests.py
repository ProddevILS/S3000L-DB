from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from arbeitszeiterfassungsapp.accounts.models import Employee
from arbeitszeiterfassungsapp.customers.models import Customer
from arbeitszeiterfassungsapp.projects.models import ActivityType, Project
from arbeitszeiterfassungsapp.time_tracking.models import TimeEntry
class ExportTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('u',password='pw'); self.emp=Employee.objects.create(user=self.user,display_name='U'); self.client.login(username='u',password='pw')
        c=Customer.objects.create(name='Kunde',short_name='K'); a=ActivityType.objects.create(name='Beratung',default_hourly_rate=100); p=Project.objects.create(customer=c,name='Projekt',short_name='P')
        TimeEntry.objects.create(employee=self.emp,customer=c,project=p,activity_type=a,date=timezone.localdate(),start_datetime=timezone.now(),end_datetime=timezone.now()+timedelta(hours=1),status='completed')
    def test_export_filter_csv(self):
        r=self.client.get('/exports/invoice/csv/?billable=1')
        self.assertEqual(r.status_code,200); self.assertIn('rechnungsanhang.csv',r['Content-Disposition'])

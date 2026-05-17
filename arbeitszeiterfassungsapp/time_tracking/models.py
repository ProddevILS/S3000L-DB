from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
class TimeEntry(models.Model):
    STATUS_RUNNING='running'; STATUS_COMPLETED='completed'; STATUS_CANCELLED='cancelled'
    SOURCE_TIMER='timer'; SOURCE_MANUAL='manual'; SOURCE_CORRECTED='corrected'
    STATUS_CHOICES=[(STATUS_RUNNING,'Laufend'),(STATUS_COMPLETED,'Abgeschlossen'),(STATUS_CANCELLED,'Storniert')]
    SOURCE_CHOICES=[(SOURCE_TIMER,'Timer'),(SOURCE_MANUAL,'Manuell'),(SOURCE_CORRECTED,'Korrigiert')]
    employee=models.ForeignKey('accounts.Employee',on_delete=models.PROTECT,related_name='time_entries')
    customer=models.ForeignKey('customers.Customer',on_delete=models.PROTECT,related_name='time_entries')
    project=models.ForeignKey('projects.Project',on_delete=models.PROTECT,null=True,blank=True,related_name='time_entries')
    activity_type=models.ForeignKey('projects.ActivityType',on_delete=models.PROTECT,related_name='time_entries')
    date=models.DateField(default=timezone.localdate)
    start_datetime=models.DateTimeField()
    end_datetime=models.DateTimeField(null=True,blank=True)
    duration_minutes=models.PositiveIntegerField(default=0)
    description=models.TextField(blank=True)
    is_pause=models.BooleanField(default=False)
    billable=models.BooleanField(default=True)
    hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    amount_net=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=STATUS_RUNNING)
    source=models.CharField(max_length=20,choices=SOURCE_CHOICES,default=SOURCE_TIMER)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-start_datetime']
    @property
    def duration_hours(self): return Decimal(self.duration_minutes)/Decimal(60)
    @property
    def hourly_rate_missing(self): return self.billable and (self.hourly_rate is None or self.hourly_rate == 0)
    def resolve_hourly_rate(self):
        if self.hourly_rate is not None: return self.hourly_rate
        if self.project_id:
            if self.activity_type and self.activity_type.name.lower()=='fahrzeit' and self.project.travel_hourly_rate is not None:
                return self.project.travel_hourly_rate
            rate=self.project.activity_rates.filter(activity_type=self.activity_type).first()
            if rate: return rate.hourly_rate
            if self.project.default_hourly_rate is not None: return self.project.default_hourly_rate
        if self.activity_type and self.activity_type.default_hourly_rate is not None: return self.activity_type.default_hourly_rate
        return Decimal('0.00')
    def recalculate(self):
        if self.end_datetime and self.start_datetime:
            delta=self.end_datetime-self.start_datetime
            self.duration_minutes=max(0, int(delta.total_seconds()//60))
        if self.billable and not self.is_pause:
            rate=self.resolve_hourly_rate(); self.hourly_rate = self.hourly_rate if self.hourly_rate is not None else rate
            self.amount_net=(Decimal(self.duration_minutes)/Decimal(60)*Decimal(self.hourly_rate or 0)).quantize(Decimal('0.01'))
        else:
            self.amount_net=Decimal('0.00')
    def save(self,*args,**kwargs):
        self.recalculate(); super().save(*args,**kwargs)
    def __str__(self): return f'{self.date} {self.customer} {self.duration_minutes} Min.'
class TimeEntryAuditLog(models.Model):
    time_entry=models.ForeignKey(TimeEntry,on_delete=models.CASCADE,related_name='audit_logs')
    changed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    changed_at=models.DateTimeField(auto_now_add=True)
    field_name=models.CharField(max_length=100)
    old_value=models.TextField(blank=True)
    new_value=models.TextField(blank=True)
    change_reason=models.TextField(blank=True)
    class Meta: ordering=['-changed_at']

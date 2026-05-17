from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import TimeEntry, TimeEntryAuditLog
from arbeitszeiterfassungsapp.accounts.models import Employee

def employee_for_user(user):
    emp, _ = Employee.objects.get_or_create(user=user, defaults={'display_name': user.get_full_name() or user.username})
    return emp

def running_entry(employee):
    return TimeEntry.objects.filter(employee=employee,status=TimeEntry.STATUS_RUNNING,is_pause=False).first()

def running_pause(employee):
    return TimeEntry.objects.filter(employee=employee,status=TimeEntry.STATUS_RUNNING,is_pause=True).first()

def validate_no_overlap(entry):
    if not entry.end_datetime: return
    qs=TimeEntry.objects.filter(employee=entry.employee,status=TimeEntry.STATUS_COMPLETED,start_datetime__lt=entry.end_datetime,end_datetime__gt=entry.start_datetime)
    if entry.pk: qs=qs.exclude(pk=entry.pk)
    if qs.exists(): raise ValidationError('Zeitbuchung überschneidet sich mit bestehenden Buchungen.')

@transaction.atomic
def start_entry(employee, customer, project, activity_type, description='', is_pause=False, source=TimeEntry.SOURCE_TIMER):
    now=timezone.now()
    if not is_pause:
        current=running_entry(employee)
        if current: stop_entry(current)
    elif running_pause(employee):
        raise ValidationError('Es läuft bereits eine Pause.')
    entry=TimeEntry.objects.create(employee=employee,customer=customer,project=project,activity_type=activity_type,date=timezone.localdate(now),start_datetime=now,description=description,is_pause=is_pause,billable=(not is_pause and activity_type.billable_default and (project.billable if project else True)),source=source)
    return entry

def stop_entry(entry):
    entry.end_datetime=timezone.now(); entry.status=TimeEntry.STATUS_COMPLETED; entry.save(); return entry

def audit_changes(entry, old, user=None, reason=''):
    fields=['customer_id','project_id','activity_type_id','date','start_datetime','end_datetime','duration_minutes','description','is_pause','billable','hourly_rate','amount_net','status','source']
    logs=[]
    for f in fields:
        oldv=getattr(old,f,None); newv=getattr(entry,f,None)
        if str(oldv)!=str(newv):
            logs.append(TimeEntryAuditLog(time_entry=entry,changed_by=user,field_name=f.replace('_id',''),old_value=str(oldv or ''),new_value=str(newv or ''),change_reason=reason))
    if logs: TimeEntryAuditLog.objects.bulk_create(logs)

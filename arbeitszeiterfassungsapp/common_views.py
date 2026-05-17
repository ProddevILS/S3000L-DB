from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone
from arbeitszeiterfassungsapp.time_tracking.models import TimeEntry
from arbeitszeiterfassungsapp.time_tracking.services import employee_for_user, running_entry

def sums(qs):
    return {'work': qs.filter(is_pause=False).aggregate(v=Sum('duration_minutes'))['v'] or 0,'pause': qs.filter(is_pause=True).aggregate(v=Sum('duration_minutes'))['v'] or 0,'billable': qs.filter(billable=True,is_pause=False).aggregate(v=Sum('duration_minutes'))['v'] or 0,'nonbillable': qs.filter(Q(billable=False)|Q(is_pause=True)).aggregate(v=Sum('duration_minutes'))['v'] or 0,'amount': qs.aggregate(v=Sum('amount_net'))['v'] or 0}
@login_required
def dashboard(request):
    emp=employee_for_user(request.user); today=timezone.localdate(); week_start=today-timezone.timedelta(days=today.weekday()); month_start=today.replace(day=1)
    return render(request,'dashboard.html',{'running':running_entry(emp),'today':sums(TimeEntry.objects.filter(employee=emp,date=today,status='completed')),'week':sums(TimeEntry.objects.filter(employee=emp,date__gte=week_start,status='completed')),'month':sums(TimeEntry.objects.filter(employee=emp,date__gte=month_start,status='completed'))})

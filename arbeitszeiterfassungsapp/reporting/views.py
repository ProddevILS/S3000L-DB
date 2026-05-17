from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from arbeitszeiterfassungsapp.time_tracking.models import TimeEntry
from arbeitszeiterfassungsapp.common_views import sums
from arbeitszeiterfassungsapp.time_tracking.services import employee_for_user

def completed(emp): return TimeEntry.objects.filter(employee=emp,status='completed')
@login_required
def reports(request):
    emp=employee_for_user(request.user); today=timezone.localdate(); week=today-timezone.timedelta(days=today.weekday()); month=today.replace(day=1)
    qs=completed(emp)
    return render(request,'reporting/reports.html',{'day':sums(qs.filter(date=today)),'week_rows':qs.filter(date__gte=week).values('date').annotate(minutes=Sum('duration_minutes'),amount=Sum('amount_net')).order_by('date'),'month_rows':qs.filter(date__gte=month).values('customer__name','project__name','activity_type__name').annotate(minutes=Sum('duration_minutes'),amount=Sum('amount_net'))})
@login_required
def project_report(request):
    emp=employee_for_user(request.user); qs=completed(emp).select_related('customer','project','activity_type')
    if request.GET.get('from'): qs=qs.filter(date__gte=request.GET['from'])
    if request.GET.get('to'): qs=qs.filter(date__lte=request.GET['to'])
    if request.GET.get('billable') in ['0','1']: qs=qs.filter(billable=request.GET['billable']=='1')
    return render(request,'reporting/filter.html',{'objects':qs})

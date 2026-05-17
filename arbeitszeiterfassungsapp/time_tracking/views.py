from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import TimerForm, TimeEntryForm
from .models import TimeEntry
from .services import audit_changes, employee_for_user, running_entry, running_pause, start_entry, stop_entry
@login_required
def timer(request):
    emp=employee_for_user(request.user); form=TimerForm(request.POST or None)
    if request.method=='POST':
        action=request.POST.get('action')
        if action in ['start','switch','pause_start'] and form.is_valid():
            start_entry(emp,form.cleaned_data['customer'],form.cleaned_data['project'],form.cleaned_data['activity_type'],form.cleaned_data['description'],is_pause=(action=='pause_start'))
            return redirect('time_tracking:timer')
        if action=='stop' and running_entry(emp): stop_entry(running_entry(emp)); return redirect('time_tracking:timer')
        if action=='pause_stop' and running_pause(emp): stop_entry(running_pause(emp)); return redirect('time_tracking:timer')
    today_entries=TimeEntry.objects.filter(employee=emp,date=timezone.localdate())
    return render(request,'time_tracking/timer.html',{'form':form,'running':running_entry(emp),'pause':running_pause(emp),'entries':today_entries})
@login_required
def entries(request):
    emp=employee_for_user(request.user); return render(request,'time_tracking/entries.html',{'objects':TimeEntry.objects.filter(employee=emp).select_related('customer','project','activity_type')[:200]})
@login_required
def entry_form(request, pk=None):
    emp=employee_for_user(request.user); obj=get_object_or_404(TimeEntry,pk=pk,employee=emp) if pk else None; old=None
    if obj: old=TimeEntry.objects.get(pk=obj.pk)
    form=TimeEntryForm(request.POST or None,instance=obj,employee=emp)
    if form.is_valid():
        entry=form.save(commit=False); entry.employee=emp; entry.status=TimeEntry.STATUS_COMPLETED; entry.source=entry.source or TimeEntry.SOURCE_MANUAL; entry.save()
        if old: audit_changes(entry,old,request.user,form.cleaned_data.get('change_reason',''))
        messages.success(request,'Zeitbuchung gespeichert.'); return redirect('time_tracking:entries')
    return render(request,'form.html',{'form':form,'title':'Zeitbuchung'})

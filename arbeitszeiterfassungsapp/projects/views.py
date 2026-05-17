from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Project, ActivityType
from .forms import ProjectForm, ActivityTypeForm
@login_required
def project_list(request): return render(request,'projects/list.html',{'objects':Project.objects.select_related('customer'),'kind':'Projekt'})
@login_required
def project_form(request, pk=None):
    obj=get_object_or_404(Project,pk=pk) if pk else None; form=ProjectForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); return redirect('projects:list')
    return render(request,'form.html',{'form':form,'title':'Projekt'})
@login_required
def project_deactivate(request, pk):
    obj=get_object_or_404(Project,pk=pk); obj.active=False; obj.save(update_fields=['active']); return redirect('projects:list')
@login_required
def activity_list(request): return render(request,'projects/activity_list.html',{'objects':ActivityType.objects.all()})
@login_required
def activity_form(request, pk=None):
    obj=get_object_or_404(ActivityType,pk=pk) if pk else None; form=ActivityTypeForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); return redirect('projects:activities')
    return render(request,'form.html',{'form':form,'title':'Tätigkeitsart'})
@login_required
def activity_deactivate(request, pk):
    obj=get_object_or_404(ActivityType,pk=pk); obj.active=False; obj.save(update_fields=['active']); return redirect('projects:activities')

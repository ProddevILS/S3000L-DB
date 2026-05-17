from django import forms
from .models import Project, ActivityType
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project; fields=['customer','name','short_name','order_number','description','start_date','end_date','default_hourly_rate','travel_hourly_rate','billable','active']; widgets={'start_date':forms.DateInput(attrs={'type':'date'}),'end_date':forms.DateInput(attrs={'type':'date'})}
class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model=ActivityType; fields=['name','description','billable_default','default_hourly_rate','unit','active']

from django import forms
from django.core.exceptions import ValidationError
from .models import TimeEntry
from .services import validate_no_overlap
class TimerForm(forms.Form):
    customer=forms.ModelChoiceField(queryset=None)
    project=forms.ModelChoiceField(queryset=None, required=False)
    activity_type=forms.ModelChoiceField(queryset=None)
    description=forms.CharField(widget=forms.Textarea(attrs={'rows':2}),required=False)
    def __init__(self,*args,**kwargs):
        from arbeitszeiterfassungsapp.customers.models import Customer
        from arbeitszeiterfassungsapp.projects.models import Project, ActivityType
        super().__init__(*args,**kwargs)
        self.fields['customer'].queryset=Customer.objects.filter(active=True)
        self.fields['project'].queryset=Project.objects.filter(active=True,customer__active=True)
        self.fields['activity_type'].queryset=ActivityType.objects.filter(active=True)
    def clean(self):
        data=super().clean(); p=data.get('project'); c=data.get('customer')
        if p and c and p.customer_id!=c.id: raise ValidationError('Projekt muss zum ausgewählten Kunden gehören.')
        return data
class TimeEntryForm(forms.ModelForm):
    overlap_confirm=forms.BooleanField(required=False,label='Überschneidung bewusst speichern')
    change_reason=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':2}),label='Änderungsgrund')
    class Meta:
        model=TimeEntry; fields=['date','start_datetime','end_datetime','customer','project','activity_type','description','is_pause','billable','hourly_rate','source']
        widgets={'date':forms.DateInput(attrs={'type':'date'}),'start_datetime':forms.DateTimeInput(attrs={'type':'datetime-local'}),'end_datetime':forms.DateTimeInput(attrs={'type':'datetime-local'})}
    def __init__(self,*args,employee=None,**kwargs): self.employee=employee; super().__init__(*args,**kwargs)
    def clean(self):
        data=super().clean(); start=data.get('start_datetime'); end=data.get('end_datetime'); p=data.get('project'); c=data.get('customer')
        if start and end and end <= start: raise ValidationError('Endzeit muss nach Startzeit liegen.')
        if p and c and p.customer_id!=c.id: raise ValidationError('Projekt muss zum Kunden gehören.')
        if start and end and self.employee:
            inst=self.instance; inst.employee=self.employee; inst.start_datetime=start; inst.end_datetime=end; inst.customer=c; inst.project=p; inst.activity_type=data.get('activity_type'); inst.billable=data.get('billable', True); inst.is_pause=data.get('is_pause', False)
            try: validate_no_overlap(inst)
            except ValidationError as exc:
                if not data.get('overlap_confirm'): raise ValidationError(str(exc)+' Bitte bestätigen, wenn trotzdem gespeichert werden soll.')
        return data

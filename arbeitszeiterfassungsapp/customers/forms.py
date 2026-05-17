from django import forms
from .models import Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer; fields=['name','short_name','billing_address','contact_person','email','notes','active']

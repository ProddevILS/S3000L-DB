from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Customer
from .forms import CustomerForm
@login_required
def list_customers(request): return render(request,'customers/list.html',{'objects':Customer.objects.all()})
@login_required
def customer_form(request, pk=None):
    obj=get_object_or_404(Customer,pk=pk) if pk else None; form=CustomerForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); return redirect('customers:list')
    return render(request,'form.html',{'form':form,'title':'Kunde'})
@login_required
def customer_detail(request, pk): return render(request,'detail.html',{'object':get_object_or_404(Customer,pk=pk),'title':'Kunde'})
@login_required
def customer_deactivate(request, pk):
    obj=get_object_or_404(Customer,pk=pk); obj.active=False; obj.save(update_fields=['active']); return redirect('customers:list')

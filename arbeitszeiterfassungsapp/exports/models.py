from django.db import models
class InvoiceExport(models.Model):
    customer=models.ForeignKey('customers.Customer',on_delete=models.PROTECT,null=True,blank=True)
    project=models.ForeignKey('projects.Project',on_delete=models.PROTECT,null=True,blank=True)
    period_start=models.DateField(); period_end=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    export_type=models.CharField(max_length=20)
    file_path=models.CharField(max_length=500,blank=True)
    total_hours=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_amount_net=models.DecimalField(max_digits=12,decimal_places=2,default=0)

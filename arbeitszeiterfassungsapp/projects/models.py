from django.db import models
class Project(models.Model):
    customer=models.ForeignKey('customers.Customer',on_delete=models.PROTECT,related_name='projects')
    name=models.CharField(max_length=200)
    short_name=models.CharField(max_length=60)
    order_number=models.CharField(max_length=100,blank=True)
    description=models.TextField(blank=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    default_hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    travel_hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    billable=models.BooleanField(default=True)
    active=models.BooleanField(default=True)
    class Meta: ordering=['customer__name','name']; unique_together=[('customer','short_name')]
    def __str__(self): return f'{self.customer.short_name} · {self.name}'
class ActivityType(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    billable_default=models.BooleanField(default=True)
    default_hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    unit=models.CharField(max_length=30,default='Stunde')
    active=models.BooleanField(default=True)
    class Meta: ordering=['name']
    def __str__(self): return self.name
class ProjectActivityRate(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='activity_rates')
    activity_type=models.ForeignKey(ActivityType,on_delete=models.CASCADE)
    hourly_rate=models.DecimalField(max_digits=8,decimal_places=2)
    class Meta: unique_together=[('project','activity_type')]
    def __str__(self): return f'{self.project} / {self.activity_type}: {self.hourly_rate}'

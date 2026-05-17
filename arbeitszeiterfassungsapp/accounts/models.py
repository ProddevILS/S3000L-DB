from django.conf import settings
from django.db import models
class Employee(models.Model):
    ROLE_ADMIN='admin'; ROLE_EMPLOYEE='employee'
    ROLE_CHOICES=[(ROLE_ADMIN,'Admin'),(ROLE_EMPLOYEE,'Mitarbeiter')]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='employee_profile')
    display_name=models.CharField(max_length=150)
    default_hourly_rate=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default=ROLE_EMPLOYEE)
    active=models.BooleanField(default=True)
    def __str__(self): return self.display_name

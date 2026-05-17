from django.db import models
class Customer(models.Model):
    name=models.CharField(max_length=200)
    short_name=models.CharField(max_length=50,unique=True)
    billing_address=models.TextField(blank=True)
    contact_person=models.CharField(max_length=150,blank=True)
    email=models.EmailField(blank=True)
    notes=models.TextField(blank=True)
    active=models.BooleanField(default=True)
    class Meta: ordering=['name']
    def __str__(self): return self.name

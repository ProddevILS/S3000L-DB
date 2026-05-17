from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True; dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[migrations.CreateModel(name='Employee',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('display_name',models.CharField(max_length=150)),('default_hourly_rate',models.DecimalField(decimal_places=2,default=0,max_digits=8)),('role',models.CharField(choices=[('admin','Admin'),('employee','Mitarbeiter')],default='employee',max_length=20)),('active',models.BooleanField(default=True)),('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='employee_profile',to=settings.AUTH_USER_MODEL))])]

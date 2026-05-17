from django.db import migrations, models
class Migration(migrations.Migration):
    initial=True; dependencies=[]
    operations=[migrations.CreateModel(name='Customer',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=200)),('short_name',models.CharField(max_length=50,unique=True)),('billing_address',models.TextField(blank=True)),('contact_person',models.CharField(blank=True,max_length=150)),('email',models.EmailField(blank=True,max_length=254)),('notes',models.TextField(blank=True)),('active',models.BooleanField(default=True))],options={'ordering':['name']})]

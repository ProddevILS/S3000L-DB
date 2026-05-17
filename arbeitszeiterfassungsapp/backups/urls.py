from django.urls import path
from . import views
app_name='backups'
urlpatterns=[path('',views.backup_home,name='home'),path('create/',views.create_backup,name='create')]

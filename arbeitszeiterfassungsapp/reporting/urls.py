from django.urls import path
from . import views
app_name='reporting'
urlpatterns=[path('',views.reports,name='reports'),path('filter/',views.project_report,name='filter')]

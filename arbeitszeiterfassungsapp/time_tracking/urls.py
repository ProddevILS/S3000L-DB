from django.urls import path
from . import views
app_name='time_tracking'
urlpatterns=[path('',views.timer,name='timer'),path('entries/',views.entries,name='entries'),path('entries/new/',views.entry_form,name='entry_new'),path('entries/<int:pk>/edit/',views.entry_form,name='entry_edit')]

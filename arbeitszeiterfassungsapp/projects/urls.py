from django.urls import path
from . import views
app_name='projects'
urlpatterns=[path('',views.project_list,name='list'),path('new/',views.project_form,name='new'),path('<int:pk>/edit/',views.project_form,name='edit'),path('<int:pk>/deactivate/',views.project_deactivate,name='deactivate'),path('activities/',views.activity_list,name='activities'),path('activities/new/',views.activity_form,name='activity_new'),path('activities/<int:pk>/edit/',views.activity_form,name='activity_edit'),path('activities/<int:pk>/deactivate/',views.activity_deactivate,name='activity_deactivate')]

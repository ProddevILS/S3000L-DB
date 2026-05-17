from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from .common_views import dashboard
urlpatterns=[path('',dashboard,name='dashboard'),path('admin/',admin.site.urls),path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),path('logout/',auth_views.LogoutView.as_view(),name='logout'),path('customers/',include('arbeitszeiterfassungsapp.customers.urls')),path('projects/',include('arbeitszeiterfassungsapp.projects.urls')),path('time/',include('arbeitszeiterfassungsapp.time_tracking.urls')),path('reports/',include('arbeitszeiterfassungsapp.reporting.urls')),path('exports/',include('arbeitszeiterfassungsapp.exports.urls')),path('backups/',include('arbeitszeiterfassungsapp.backups.urls'))]

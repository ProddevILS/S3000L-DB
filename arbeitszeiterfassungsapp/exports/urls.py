from django.urls import path
from . import views
app_name='exports'
urlpatterns=[path('',views.exports_home,name='home'),path('invoice/<str:fmt>/',views.invoice_export,name='invoice'),path('lexware/',views.lexware_csv,name='lexware')]

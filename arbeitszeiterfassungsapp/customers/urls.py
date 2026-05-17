from django.urls import path
from . import views
app_name='customers'
urlpatterns=[path('',views.list_customers,name='list'),path('new/',views.customer_form,name='new'),path('<int:pk>/',views.customer_detail,name='detail'),path('<int:pk>/edit/',views.customer_form,name='edit'),path('<int:pk>/deactivate/',views.customer_deactivate,name='deactivate')]

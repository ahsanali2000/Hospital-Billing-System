from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='/'),
    path('home',views.home,name='home'),
    path('error', views.error, name='Error'),
    path('doc', views.doc, name='Doctor'),
    path('invoice',views.invoice,name='invoice')
]
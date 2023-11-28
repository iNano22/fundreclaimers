from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name="home"),
path('crm/', views.crm, name="crm"),
path('upload_csv/', views.upload_csv, name='upload_csv'),
]
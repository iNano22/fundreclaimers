from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name="home"),
path('crm/', views.crm, name="crm"),
path('upload/', views.upload, name='upload'),
path('edit/<str:id>/', views.edit, name="edit"),
path('delete/<str:id>/', views.delete, name="delete"),

]
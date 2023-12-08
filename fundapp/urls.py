from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
path('', views.home, name="home"),
path('crm/', views.crm, name="crm"),
path('upload/', views.upload, name='upload'),
path('edit/<str:id>/', views.edit, name="edit"),
path('delete/<str:id>/', views.delete, name="delete"),
path('login_user/', views.login_user, name='login_user'),
path('signin/', views.signin, name='signin'),
path('signup/', views.signup, name='signup'),
path('signout/', views.signout, name='signout'),
path('registration/', views.registration, name='registration'),

]
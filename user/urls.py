from django.contrib import admin
from django.urls import path, re_path
from user import views

urlpatterns = [
    path(r'register/', views.register),
    path(r'register_exist/', views.register_exist),
    path(r'login/', views.login),
    path(r'info/', views.info),
    path(r'order/', views.order),
    path(r'site/', views.site),
    path(r'logout/', views.logout),

]
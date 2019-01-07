from django.contrib import admin
from django.urls import path, re_path
from order import views
urlpatterns = [
        re_path('from_(\w+)/', views.order),
        path('add_order/', views.add_order),
        re_path(r'pay_(\d+)/', views.pay),
]
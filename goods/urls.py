from django.contrib import admin
from django.urls import path, re_path
from goods import views
urlpatterns = [
    path(r'home/', views.home),
    re_path(r'list_(\w+)_(\w+)_(\d+)/', views.goods_list),
    re_path(r'detail_(\w+)_(\d+)/', views.detail),
    path('search/', views.search),
]
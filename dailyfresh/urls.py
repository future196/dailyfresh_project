"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from user import urls as user
from goods import urls as goods
from cart import urls as cart
from order import urls as order
from goods import views

urlpatterns = [
    path(r'', views.home),
    path(r'admin/', admin.site.urls),
    path(r'user/', include(user)),
    path(r'goods/', include(goods)),
    path(r'tinymce/', include('tinymce.urls')),
    path(r'cart/', include(cart)),
    path(r'order/', include(order)),
]

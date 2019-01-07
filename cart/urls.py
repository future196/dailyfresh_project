from django.urls import path, re_path
from cart import views as cart

urlpatterns = [
    path(r'', cart.cart),
    re_path(r'add_cart_(\d+)_(\d+)/', cart.add_cart),
    re_path(r'delete_(\d+)/', cart.delete_cart),
    re_path(r'num_change_(\d+)_(\w+)_(\d+)', cart.num_change),
]
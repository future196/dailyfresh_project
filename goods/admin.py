from django.contrib import admin
from user.models import User
from goods.models import Type, Goods
from cart.models import Cart
from order.models import Order, OrderDetail

# Register your models here.
admin.site.register([Type, Goods, Cart,Order, OrderDetail])
admin.site.register(User)
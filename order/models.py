from django.db import models

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    is_pay = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    address = models.CharField(max_length=150, default='')
    pay = models.IntegerField(default=0)


class OrderDetail(models.Model):
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()
from django.db import models
from goods.models import Goods

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE)
    count = models.IntegerField()
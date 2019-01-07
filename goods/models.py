from django.db import models
# from tinymce.models import HTMLField
# Create your models here.

class Type(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Goods(models.Model):
    name = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='goods')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    unit = models.CharField(max_length=20, default='500g')
    hits = models.IntegerField()
    introduction = models.CharField(max_length=200)
    stock = models.IntegerField()
    # detail = HTMLField()
    detail = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=52)
    telephone = models.CharField(max_length=11, default="")
    address = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=30,)
    zip_code = models.CharField(max_length=6, default="")
    receive_user = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class contact(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name

class users_data(models.Model):
    f_key = models.ForeignKey(User,on_delete=models.CASCADE)
    data = models.TextField()
    fetch_done = models.BooleanField()

    def __str__(self):
        temp = str(self.f_key)
        return temp

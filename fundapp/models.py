from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    source = models.CharField(max_length=100)
    class Meta:
        app_label = 'fundapp'
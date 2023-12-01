from django.db import models

# Create your models here.
class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    source = models.CharField(max_length=100)
    class Meta:
        app_label = 'fundapp'
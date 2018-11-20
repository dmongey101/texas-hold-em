from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Table(models.Model):
    
    name = models.CharField(max_length=200)
    blinds = models.IntegerField(default=10)
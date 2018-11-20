from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Table(models.Model):
    
    name = models.CharField(max_length=50)
    blinds = models.IntegerField(default=10)
    player = models.OneToOneField(User, default=1, on_delete=models.PROTECT)
    
class Player(models.Model):
    
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, related_name="players_table", on_delete=models.CASCADE)
    chips = models.IntegerField(default=1000)
    card1 = models.CharField(max_length=3)
    card2 = models.CharField(max_length=3)
    
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Table(models.Model):
    
    name = models.CharField(max_length=50)
    blinds = models.IntegerField(default=10)
    current_player = models.OneToOneField(User, on_delete=models.CASCADE, related_name='current_player', default=1, null=False)
    
    
    def __str__(self):
        return self.name
        
class Player(models.Model):
    
    user = models.OneToOneField(User, related_name='player', on_delete=models.CASCADE, null=False, default=1)
    table = models.ForeignKey(Table, default=1, on_delete=models.CASCADE)
    chips = models.IntegerField(default=1000)
    card_1 = models.CharField(max_length=3, default="")
    card_2 = models.CharField(max_length=3, default="")
    
    def __str__(self):
        return self.user.username 
    
    

class Hand(models.Model):
    
    table = models.ForeignKey(Table, related_name="table_hand", on_delete=models.CASCADE)
    card_1 = models.CharField(max_length=3)
    card_2 = models.CharField(max_length=3)
    card_3 = models.CharField(max_length=3)
    card_4 = models.CharField(max_length=3)
    card_5 = models.CharField(max_length=3)
    players = models.ManyToManyField(Player)
    pot = models.IntegerField(default=0)
    preflop_betting = models.IntegerField(default=0)
    flop_betting = models.IntegerField(default=0)
    turn_betting = models.IntegerField(default=0)
    river_betting = models.IntegerField(default=0)
    winner = models.ManyToManyField(Player, related_name="winning_hands")
    
    
    def __str__(self):
        return "{0} : Hand {1}".format(self.table.name, self.id)
    
    
    
    
    
    
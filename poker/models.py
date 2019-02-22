from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Table(models.Model):
    
    name = models.CharField(max_length=50)
    no_of_players = models.IntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(8)])
    blinds = models.IntegerField(default=10)
    is_active = models.BooleanField(default=False)
    dealer = models.IntegerField(default=-1)
    big_blind = models.IntegerField(default=1)
    small_blind = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
        
class Player(models.Model):
    
    user = models.OneToOneField(User, related_name='player', on_delete=models.CASCADE, null=False, default=1)
    table = models.ForeignKey(Table, default=1, related_name='players', on_delete=models.CASCADE)
    chips = models.PositiveIntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    seat_num = models.IntegerField(default=0)
    card_1 = models.CharField(max_length=3, default="")
    card_2 = models.CharField(max_length=3, default="")
    player_pot = models.IntegerField(default=0)
    
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
    current_player = models.IntegerField(default=0)
    raise_amount = models.IntegerField(default=0)
    current_bet = models.IntegerField(default=0)
    player_pot = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    check_no = models.IntegerField(default=1)
    winner = models.ManyToManyField(Player, related_name="winning_hands")
    
    
    def __str__(self):
        return "{0} : Hand {1}".format(self.table.name, self.id)
    
    
    
    
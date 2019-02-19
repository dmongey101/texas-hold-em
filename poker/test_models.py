from django.test import TestCase
from .models import Table, Player, Hand
from django.contrib.auth.models import User
# Create your tests here.

class TestPokerModel(TestCase):
        
    def test_table_item_as_string(self):
        table = Table(name="Table 1")
        self.assertEqual("Table 1", str(table))


    def test_player_item_as_string(self):
        user = User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        player = Player()
        player.user = user
        player.save()
        self.assertEqual("test", str(player))


    def test_hand_item_as_string(self):
        table = Table(name="Table 1")
        table.save()
        hand = Hand(table=table)
        hand.save()
        self.assertEqual("{0} : Hand {1}".format(table.name, hand.id), str(table) + " : Hand " + str(hand.id))
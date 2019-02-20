from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Table, Hand, Player
from django.contrib.auth.models import User

# Create your tests here.

class TestViews(TestCase):
    
    
    def test_get_homepage(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "poker/index.html")


    def test_get_create_table_page(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        page = self.client.get("/poker/create_table", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "poker/create_table_form.html")


    def test_post_create_table(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        response = self.client.post("/poker/create_table/", {'name':"Test Table", 'blinds': 10, 'no_of_players': 2})
        table = get_object_or_404(Table, pk=1)
        self.assertRedirects(response, '/poker/view_table/{0}'.format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_get_find_table_page(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        page = self.client.get("/poker/find_table", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "poker/find_table.html")


    def test_get_view_table_page(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        table = Table(name="Table 1")
        table.save()
        page = self.client.get("/poker/view_table/{0}".format(table.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "poker/view_table.html")


    def test_redirect_player_to_view_table_when_they_join(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        table = Table(name="Table 1")
        table.save()
        response = self.client.post("/poker/table/join/{0}".format(table.id))
        self.assertRedirects(response, '/poker/view_table/{0}'.format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_table_is_deleted_when_game_is_over(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        table = Table(name='Table 1')
        table.is_active = True
        table.save()
        response = self.client.post("/poker/view_table/{0}".format(table.id))
        self.assertRedirects(response, "/poker/find_table/", status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_get_current_hand_page(self):
        table = Table(name="Table 1")
        table.save()
        hand = Hand(table=table)
        hand.save()
        page = self.client.get("/poker/table/current_hand/{0}".format(table.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "poker/current_hand.html")


    def test_player_is_deleted_redirected_to_find_table_when_no_chips(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        player = Player()
        player.chips = 0
        player.save()
        response = self.client.get('/poker/table/current_hand/{0}'.format(table.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/poker/find_table/')


    def test_delete_player_and_redirect_to_find_table_when_they_leave(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        table = Table(name='Table 1')
        table.save()
        player = Player()
        player.save()
        response = self.client.post("/poker/table/leave/{0}/{1}".format(table.id, player.id))
        self.assertRedirects(response, '/poker/find_table/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_dealing(self):
        table = Table(name='Table 1')
        table.save()
        response = self.client.post("/poker/table/hand/deal/{0}".format(table.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_folding(self):
        User.objects.create_user(username='test', email='test@example.com', password='Madetotest')
        self.client.login(username='test', password='Madetotest')
        player = Player()
        player.save()
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        response = self.client.post("/poker/game/hand/fold/{0}/{1}".format(hand.id, player.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_betting(self):
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        player =  Player()
        player.save()
        response = self.client.post("/poker/game/hand/bet/{0}/{1}/{2}".format(table.id, hand.id, player.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_raising(self):
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        player =  Player()
        player.save()
        response = self.client.post("/poker/game/hand/raise/{0}/{1}/{2}".format(table.id, hand.id, player.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_calling(self):
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        player =  Player()
        player.save()
        response = self.client.post("/poker/game/hand/call/{0}/{1}/{2}".format(table.id, hand.id, player.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_redirect_to_current_hand_after_checking(self):
        table = Table(name='Table 1')
        table.save()
        hand = Hand(table=table)
        hand.save()
        player =  Player()
        player.save()
        response = self.client.post("/poker/game/hand/check/{0}/{1}/{2}".format(table.id, hand.id, player.id))
        self.assertRedirects(response, "/poker/table/current_hand/{0}".format(table.id), status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        
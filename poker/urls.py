from django.urls import path
from poker.views import create_table, find_table, view_table, get_current_hand, join_table, leave_table, deal_cards, fold_hand, bet, raise_bet, call_bet

urlpatterns = [
    path('create_table/', create_table, name="create_table"),
    path('find_table/', find_table, name='find_table'),
    path('view_table/<int:id>', view_table, name="view_table"),
    path('table/join/<int:id>', join_table, name='join_table'),
    path('table/leave/<int:table_id>/<int:player_id>', leave_table, name='leave_table'),
    path('table/current_hand/<int:id>', get_current_hand, name='current_hand'),
    path('table/hand/deal/<int:id>', deal_cards, name='deal'),
    path('game/hand/fold/<int:hand_id>/<int:player_id>', fold_hand, name='fold'),
    path('game/hand/bet/<int:table_id>/<int:hand_id>/<int:player_id>', bet, name='bet'),
    path('game/hand/raise/<int:table_id>/<int:hand_id>/<int:player_id>', raise_bet, name='raise'),
    path('game/hand/call/<int:table_id>/<int:hand_id>/<int:player_id>', call_bet, name='call'),
 ]
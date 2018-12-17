from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .holdem import Poker
from .deck import Card
from .forms import CreateTableForm
from .models import Table, Player, Hand
import sys 
import random

def show_index(request):
    return render(request, "poker/index.html")
    
@login_required
def create_table(request):
    if request.method=="POST":
        form = CreateTableForm(request.POST)
        table = form.save(commit=False)
        table.owner = request.user
        table.save()
        return redirect('view_table', table.id)
    else:
        form = CreateTableForm()
        return render(request, "poker/create_table_form.html", {"form" : form})
        
def find_table(request):
    tables = Table.objects.all()
    return render(request, "poker/find_table.html", {"tables" : tables})
        
def view_table(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.last()
    
    if len(players) == table.no_of_players:
        return redirect(get_current_hand, id)
        
    return render(request, "poker/view_table.html", {"table" : table, "players" : players, "hand" : hand})

def get_current_hand(request, id):  
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.last()
    no_of_preflop_players = len(players)
    no_of_flop_players = len(players) * 2 
    no_of_turn_players = len(players) * 3
    no_of_river_players = len(players) * 4
    number_of_players = len(players)
    poker = Poker(number_of_players, False)
    card1 = Card.from_str(hand.card_1)
    card2 = Card.from_str(hand.card_2)
    card3 = Card.from_str(hand.card_3)
    card4 = Card.from_str(hand.card_4)
    card5 = Card.from_str(hand.card_5)
    community_cards = [card1, card2, card3, card4, card5]
    players_hands = []
    active_players = []
    active_players.reverse()
    
    for player in players:
        if (hand.check_no == len(players) * 4 and 
            player.is_active) :
                players_hands.append([Card.from_str(player.card_1), Card.from_str(player.card_2)])
                active_players.append(player)
                
                if player.chips == 0:
                    p = Player.objects.get(id=player.id)
                    p.delete()
                    return redirect('current_hand', id)
                
    if hand.check_no == len(players) * 4:
        results = poker.determine_score(community_cards, players_hands)
        determine_winner = poker.determine_winner(results)
        
    for player in players:
        if hand.check_no == len(players) * 4: 
            if determine_winner in range(len(active_players)):
                winner = active_players[determine_winner]
                hand.winner.add(winner)
            else:
                for i in determine_winner:
                    
                    winner = active_players[i]
                    hand.winner.add(winner)
        if player in hand.winner.all():
            if len(hand.winner.all()) > 1:
                print(hand.pot/len(hand.winner.all()))
                player.chips += (hand.pot/len(hand.winner.all()))
                
            elif player == winner:
                player.chips += hand.pot
                hand.pot = 0
        
    if (hand.check_no == len(players) or 
        hand.check_no == len(players) * 2 or 
        hand.check_no == len(players) * 3 or 
        hand.check_no == len(players) * 4) :
            
        hand.current_bet = 0
        hand.raise_amount = 0
        hand.player_pot = 0
        
        for player in players:
            player.player_pot = 0
            player.save()
    
    for player in players:
        if player.seat_num == hand.current_player:
            if not player.is_active:
                hand.current_player += 1
                hand.check_no += 1
        
        if hand.current_player >= len(players):
            hand.current_player = 0
        hand.save()
        
    context = {"table" : table, "players" : players, "hand" : hand,
                "no_of_preflop_players" : no_of_preflop_players, 
                "no_of_flop_players" : no_of_flop_players,
                "no_of_turn_players" : no_of_turn_players, 
                "no_of_river_players" : no_of_river_players}
    
    return render(request, "poker/current_hand.html", context)

def join_table(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    player = Player()
    player.table_id = id
    player.user = request.user
    player.save()
    
    if len(players) == table.no_of_players:
        table.is_active = True
        table.save()
        return deal_cards(request, id)
    return redirect('view_table', id)
    
def leave_table(request, table_id, player_id):
    table = Table.objects.get(id=table_id)
    player = Player.objects.get(id=player_id).delete()
    return redirect('view_table', table_id)
    
def deal_cards(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    number_of_players = len(players)
    poker = Poker(number_of_players, False)
    poker.shuffle()
    poker.cut(random.randint(1,51))
    hand = Hand()
    hand.table_id = table.id
    for i in range(2):
        cards = poker.distribute()
        p = 0
        for player in players:
            if i == 0:
                player.card_1 = cards[p][0]
            elif i == 1:
                player.card_2 = cards[p][0]
            p+=1
        
        for player in players:
            player.is_active = True
            player.save()
    poker.burnOne()
    card1 = poker.getOne()
    hand.card_1 = card1[0]
    card2 = poker.getOne()
    hand.card_2 = card2[0]
    card3 = poker.getOne()
    hand.card_3 = card3[0]
    poker.burnOne()
    card4 = poker.getOne()
    hand.card_4 = card4[0]
    poker.burnOne()
    card5 = poker.getOne()
    hand.card_5 = card5[0]
    hand.save()
    for player in players:
        hand.players.add(player)
        
    for index, item in enumerate(players):
        item.seat_num = index
        item.save()
    
    return redirect('current_hand', id)
        
def fold_hand(request, hand_id, player_id):
    players = Player.objects.filter(id=hand_id)
    p = Player.objects.get(id=player_id)
    p.is_active = False
    p.save()
    hand = Hand.objects.get(id=hand_id)
    hand.players.remove(p)
    hand.current_player += 1
    hand.check_no += 1
    hand.save()
    table_id = hand.table_id
    
    return redirect('current_hand', table_id)

def bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST['bet']
    if int(amount) > player.chips:
        return HttpResponse('Not enough chips')
    hand.pot += int(amount)
    hand.current_bet += int(amount)
    if  hand.check_no < len(players):
        hand.check_no = 1
        
    if (hand.check_no >= len(players) and 
        hand.check_no < (len(players) * 2)) :
            
        hand.check_no = len(players) + 1
        
    if (hand.check_no >= (len(players) * 2) and 
        hand.check_no < (len(players) * 3)) :
            
        hand.check_no = (len(players) * 2) + 1
        
    if (hand.check_no >= (len(players) * 3) and 
        hand.check_no < (len(players) * 4)) :
            
        hand.check_no = (len(players) * 3) + 1
        
    if  hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
        
    player.player_pot += int(amount)
    hand.player_pot = player.player_pot
    player.chips -= int(amount)
    player.save()
    hand.save()
    
    return redirect('current_hand', table_id)
    
def raise_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST['raise']
    if int(amount) > player.chips:
        return HttpResponse('Not enough chips')
    old_player_pot = player.player_pot
    hand.raise_amount += int(amount)
    hand.current_bet += int(amount)
    player.player_pot += (hand.current_bet - player.player_pot)
    hand.player_pot = player.player_pot
    player.chips -= (player.player_pot - old_player_pot)
    player.save()
    hand.pot +=  (player.player_pot - old_player_pot)
    
    if hand.check_no < len(players):
        hand.check_no = 1
    
    if (hand.check_no >= len(players) and 
        hand.check_no < (len(players) * 2)) :
            
        hand.check_no = len(players) + 1
    
    if (hand.check_no >= (len(players) * 2) and
        hand.check_no < (len(players) * 3)) :
            
        hand.check_no = (len(players) * 2) + 1
    
    if (hand.check_no >= (len(players) * 3) and 
        hand.check_no < (len(players) * 4)) :
            
        hand.check_no = (len(players) * 3) + 1
    
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
    
    hand.save()
    
    return redirect('current_hand', table_id)
    
def call_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    if hand.current_bet > player.chips:
        return HttpResponse('Not enough chips')
    if hand.raise_amount != 0:
        hand.raise_amount = hand.current_bet - hand.raise_amount
    else:
        hand.raise_amount = 0
    old_player_pot = player.player_pot
    hand.current_bet -= hand.raise_amount
    player.player_pot = hand.player_pot
    player.chips -= (player.player_pot - old_player_pot)
    hand.pot += (player.player_pot - old_player_pot)
    hand.check_no += 1
    
    if (hand.check_no == len(players) or 
        hand.check_no == len(players) * 2 or 
        hand.check_no == len(players) * 3 or 
        hand.check_no == len(players) * 4) :
            
        hand.current_bet = 0
        hand.raise_amount = 0
        hand.player_pot = 0
            
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
        
    hand.save()
    player.save()
    
    if hand.check_no == len(players) * 4:
        for winner in hand.winner.all():
            for player in players:
                if str(player.user) == str(winner):
                    player.chips += hand.pot
                    player.save()
                    hand.current_bet = 0
                    hand.pot = 0
                    hand.save()
                    
    return redirect('current_hand', table_id)
    
def check_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    hand.check_no += 1
    
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
        
    if hand.check_no == len(players) * 4:
        for winner in hand.winner.all():
            for player in players:
                if str(player.user) == str(winner):
                    player.chips += hand.pot
                    player.save()
                    hand.current_bet = 0
                    hand.pot = 0
    hand.save()
    return redirect('current_hand', table_id)
    

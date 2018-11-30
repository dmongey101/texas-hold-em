from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .holdem import Poker
from .deck import Card
from .forms import CreateTableForm, CreatePlayerForm, CreateHandForm
from .models import Table, Player, Hand
import sys, random

def show_index(request):
    return render(request, "poker/index.html")
    
@login_required
def create_table(request):
    if request.method=="POST":
        form = CreateTableForm(request.POST)
        table = form.save(commit=False)
        table.owner = request.user
        table.save()
        player = Player()
        player.table_id = table.id
        player.user = request.user
        player.save()
        return redirect('view_table', table.id)
    else:
        form = CreateTableForm()
        return render(request, "poker/create_table_form.html", {'form': form})
        
def find_table(request):
    tables = Table.objects.all()
    return render(request, "poker/find_table.html", {"tables" : tables})
        
def view_table(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.last()
    return render(request, "poker/view_table.html", {"table" : table, "players" : players, "hand" : hand})

def get_current_hand(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.last()
    return render(request, "poker/current_hand.html", {"table" : table, "players" : players, "hand" : hand})

def join_table(request, id):
    player = Player()
    player.table_id = id
    player.user = request.user
    player.save()
    return redirect('current_hand', id)
    
def leave_table(request, table_id, player_id):
    table = Table.objects.get(id=table_id)
    player = Player.objects.get(id=player_id).delete()
    return redirect('view_table', table_id)
    
def deal_cards(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    debug = False
    number_of_players = len(players)
    poker = Poker(number_of_players, debug)
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
    player = Player()
    for player in players:
        hand.players.add(player)
            
    # for index, item in enumerate(players):
    #     print(players[1])
    return redirect('current_hand', id)
        
def fold_hand(request, hand_id, player_id):
    p = Player.objects.get(id=player_id)
    hand = Hand.objects.get(id=hand_id)
    hand.players.remove(p)
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
    hand.save()
    p.is_active = False
    p.save()
    table_id = hand.table_id
    return redirect('current_hand', table_id)

def bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST['bet']
    hand.pot += int(amount)
    hand.sub_pot += int(amount)
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
    hand.save()
    player.chips -= int(amount)
    player.save()
    return redirect('current_hand', table_id)
    
def raise_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST['raise']
    player.chips -= (int(amount) +  hand.sub_pot)
    player.save()
    hand.pot += (int(amount) +  hand.sub_pot)
    hand.sub_pot += int(amount)
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
    call = hand.sub_pot
    hand.pot += hand.sub_pot
    player.chips -= call
    player.save()
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
    hand.save()
    return redirect('current_hand', table_id)
    
def check_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else: 
        hand.current_player += 1
    hand.save()
    return redirect('current_hand', table_id)

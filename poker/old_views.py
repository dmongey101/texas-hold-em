from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .holdem import Poker
from .deck import Card
from .forms import CreateTableForm, CreatePlayerForm, CreateHandForm
from .models import Table, Player, Hand
import sys, random



# Create your views here.

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
        return redirect(start_game,table.id)
    else:
        form = CreateTableForm()
        return render(request, "poker/create_table_form.html", {'form': form})
        
def find_table(request):
    tables = Table.objects.all()
    return render(request, "poker/find_table.html", {"tables" : tables})
    
def create_player(request, table_id):
    player = Player()
    player.table_id = table_id
    player.user = request.user
    player.save()
    return redirect(start_game, table_id)  
    
def start_game(request, id):
    if request.method=="POST":
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
        
        return redirect(start_game, id)

    else:
        table = get_object_or_404(Table, pk=id)
        players = Player.objects.filter(table=table)
        debug = False
        number_of_players = len(players)
        poker = Poker(number_of_players, debug)
        hand = Hand.objects.last()
        if Hand.objects.filter(table=table).exists():
            for player in players:
                hand.players.add(player)
        # card1 = Card.from_str(hand.card_1)
        # card2 = Card.from_str(hand.card_2)
        # card3 = Card.from_str(hand.card_3)
        # card4 = Card.from_str(hand.card_4)
        # card5 = Card.from_str(hand.card_5)
        # community_cards = [card1, card2, card3, card4, card5]
        # players_hands = []
        # for player in players:
        #     players_hands.append([Card.from_str(player.card_1), Card.from_str(player.card_2)])
        # results = poker.determine_score(community_cards, players_hands)
        # determine_winner = poker.determine_winner(results)
        # winner = players[determine_winner]
        # hand.winner.add(winner)
        hand.save()    
            
        return render(request, "poker/game.html", {"table" : table, "players" : players, "hand" : hand})


def fold_hand(request, hand_id, player_id):
    p = Player.objects.get(id=player_id)
    hand = Hand.objects.get(id=hand_id)
    hand.players.remove(p)
    hand.save()
    table_id = hand.table_id
    return redirect(start_game, table_id)
    

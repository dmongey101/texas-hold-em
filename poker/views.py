from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .holdem import Poker
from .forms import CreateTableForm
from .models import Table
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
        return redirect(get_table, request.POST['name'])
    else:
        form = CreateTableForm()
        return render(request, "poker/create_table_form.html", {'form': form})
        
def find_table(request):
    tables = Table.objects.all()
    return render(request, "poker/find_table.html", {"tables" : tables})

def view_table(request, name):
    table = Table.objects.get(name=name)
    players = Player.objects.all()

    print(table.hands.count())
    if table.hands.count() > 0:
        hand = table.hands[0]
        number_of_players = hand.players.count()
    else:
        number_of_players = 0
    
    debug = False
    poker = Poker(number_of_players, debug)
    poker.shuffle()
    poker.cut(random.randint(1,51))
    players_hand = poker.distribute()
    community_cards = []
    return render(request, "poker/view_table.html", {"table" : table, "players" : players})
    


    
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .holdem import Poker
from .deck import Card
from .forms import CreateTableForm
from .models import Table, Player, Hand
import sys
import random


# ------ Homepage --------
def show_index(request):
    return render(request, "poker/index.html")


# ----- Create table form ------
@login_required
def create_table(request):
    if request.method == "POST":
        form = CreateTableForm(request.POST)
        table = form.save(commit=False)
        table.owner = request.user
        if form.is_valid():
            table.save()
        return redirect('view_table', table.id)
    else:
        form = CreateTableForm()
        return render(request, "poker/create_table_form.html", {"form": form})


# ------- List of all live tables --------
@login_required
def find_table(request):
    tables = Table.objects.all()
    no_of_tables = len(tables)
    context = {"tables": tables, "no_of_tables": no_of_tables}
    return render(request, "poker/find_table.html", context)


# ----- Shows details of the table and players in the table --------
@login_required
def view_table(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)

    player_list = []
    for player in players:
        player_list.append(player.user)

    # Delete the table when game is over
    if table.is_active and len(players) == 0:
        table.delete()
        return redirect(find_table)

    # Redirects to the table when all players have joined
    if len(players) == table.no_of_players:
        return redirect(get_current_hand, id)

    context = {"table": table, "players": players,
              "player_list": player_list}

    return render(request, "poker/view_table.html", context)


# -------- Shows any particular live game --------
def get_current_hand(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.last()
    number_of_players = len(players)
    no_of_flop_players = number_of_players * 2
    no_of_turn_players = number_of_players * 3
    no_of_river_players = number_of_players * 4
    poker = Poker(number_of_players, False)
    card1 = Card.from_str(hand.card_1)
    card2 = Card.from_str(hand.card_2)
    card3 = Card.from_str(hand.card_3)
    card4 = Card.from_str(hand.card_4)
    card5 = Card.from_str(hand.card_5)
    community_cards = [card1, card2, card3, card4, card5]
    players_hands = []

    # When all but one players fold, final player is determined winner
    unfolded_player = []
    for player in players:
        if player.is_active:
            unfolded_player.append(player)

    if len(unfolded_player) == 1:
        hand.check_no = no_of_river_players

    active_players = []
    active_players.reverse()
    # Players hands left at the end of a hand
    # are put into a list to determine a winner
    for player in players:
        if (hand.check_no == no_of_river_players and
          player.is_active):
            players_hands.append([Card.from_str(player.card_1),
                                  Card.from_str(player.card_2)])
            active_players.append(player)
    # Dealing with the end of the hand
    if hand.check_no == no_of_river_players:
        results = poker.determine_score(community_cards, players_hands)
        determine_winner = poker.determine_winner(results)

        # If there is only one winner
        if determine_winner in range(len(active_players)):
            winner = active_players[determine_winner]
            hand.winner.add(winner)
        # If there are more than one winners
        else:
            for i in determine_winner:
                winner = active_players[i]
                hand.winner.add(winner)

        for player in players:
            if player in hand.winner.all():
                # Splits the pot when there are more than one winners
                if len(hand.winner.all()) > 1:
                    player.chips += (hand.pot/len(hand.winner.all()))

                # Player recieves the whole pot when only one winner
                else:
                    player.chips += hand.pot

            # Deletes a player when they're out of chips
            if player.chips == 0:
                p = Player.objects.get(id=player.id)
                p.delete()
                return redirect(find_table)
        hand.pot = 0
    # Reset of values after each round of betting
    if (hand.check_no == number_of_players or
      hand.check_no == no_of_flop_players or
      hand.check_no == no_of_turn_players or
      hand.check_no == no_of_river_players):

        hand.current_bet = 0
        hand.raise_amount = 0
        hand.player_pot = 0
        # Betting always starts with small blind
        hand.current_player = table.small_blind

        for player in players:
            player.player_pot = 0
            player.save()

    # Skipping folded players
    for player in players:
        if player.seat_num == hand.current_player:
            if not player.is_active:
                hand.current_player += 1
                if hand.check_no < no_of_river_players:
                    hand.check_no += 1
    # Brings betting back to first player when the end of table is reached
    if hand.current_player >= len(players):
        hand.current_player = 0
    hand.save()

    # Skipping empty seats
    player_seats = []
    for player in players:
        player_seats.append(player.seat_num)

    if hand.current_player not in player_seats:
        hand.current_player += 1
    if table.dealer not in player_seats:
        table.dealer += 1
        table.small_blind += 1
        table.big_blind += 1
    if table.small_blind not in player_seats:
        table.small_blind += 1
        table.big_blind += 1
    if table.big_blind not in player_seats:
        table.big_blind += 1
    if table.dealer >= number_of_players:
        table.dealer = 0
    if table.big_blind >= number_of_players:
        table.big_blind = 0
    if table.small_blind >= number_of_players:
        table.small_blind = 0
    hand.save()
    table.save()
    # Deal button will appear on the screen of the
    # players who's turn it is to deal
    dealer = table.dealer + 1
    if dealer >= number_of_players:
        dealer = 0

    big_blind_check = number_of_players - 1

    context = {"table": table, "players": players, "hand": hand,
              "number_of_players": number_of_players,
              "no_of_flop_players": no_of_flop_players,
              "no_of_turn_players": no_of_turn_players,
              "no_of_river_players": no_of_river_players,
              "dealer": dealer, "big_blind_check": big_blind_check
              }
    return render(request, "poker/current_hand.html", context)


# ------- Creates a player for a table ---------
def join_table(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    player = Player()
    player.table_id = id
    player.user = request.user
    player.save()

    # Activates table when full and assigns a player a seat
    if len(players) == table.no_of_players:
        table.is_active = True
        table.save()
        for index, player in enumerate(players):
            player.seat_num = index
            player.save()
        return redirect('deal', id)
    return redirect('view_table', id)


# ------- Deletes a player when the leave -------
def leave_table(request, table_id, hand_id, player_id):
    table = Table.objects.get(id=table_id)
    players = Player.objects.filter(table=table)
    hand = Hand.objects.get(id=hand_id)
    hand.check_no -= (hand.check_no / len(players))
    hand.save()
    player = Player.objects.get(id=player_id).delete()
    return redirect(find_table)


# -- Deals two cards to every player and deals 5 community cards --
def deal_cards(request, id):
    table = get_object_or_404(Table, pk=id)
    players = Player.objects.filter(table=table)
    number_of_players = len(players)
    poker = Poker(number_of_players, False)
    poker.shuffle()
    poker.cut(random.randint(1, 51))
    hand = Hand()
    hand.table_id = table.id
    table.dealer += 1  # First dealer will be player 0

    # Ensures there will be no wrong dealer, big/small blind
    if table.dealer >= number_of_players:
        table.dealer = 0
    table.big_blind += 1
    if table.big_blind >= number_of_players:
        table.big_blind = 0
    table.small_blind += 1
    if table.small_blind >= number_of_players:
        table.small_blind = 0
    table.save()

    # Adding big and small blinds to the pot
    for player in players:
        if player.seat_num == table.small_blind:
            small_blind = (table.blinds / 2)
            player.chips -= small_blind
            player.player_pot += small_blind
            hand.pot += small_blind

        if player.seat_num == table.big_blind:
            big_blind = table.blinds
            player.chips -= big_blind
            player.player_pot += big_blind
            hand.player_pot += big_blind
            hand.pot += big_blind
            player.save()

    hand.current_bet = table.blinds
    hand.current_player = table.big_blind + 1

    # Distributes two cards to every player
    for i in range(2):
        cards = poker.distribute()
        p = 0
        for player in players:
            if i == 0:
                player.card_1 = cards[p][0]
            elif i == 1:
                player.card_2 = cards[p][0]
            p += 1
            player.is_active = True
            player.save()

    # Deals the 5 community cards
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
    
    # Ensures big blind has option to raise in pre-flop betting
    hand.check_no = 0
    hand.save()

    # Adds players to the hand
    for player in players:
        hand.players.add(player)

    return redirect('current_hand', id)


# ------ Removes a player from a hand -------
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


# -------   Initial Bet ----------
def bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST.get('bet', 0)
    # When a player doesn't have enough chips
    if int(amount) > player.chips:
        return HttpResponse('Not enough chips')

    hand.pot += int(amount)
    hand.current_bet += int(amount)

    # The next four if statements reset the check number
    # when a bet is made to work accordingly with the games checking system
    if hand.check_no < len(players):
        hand.check_no = 1

    if (hand.check_no >= len(players) and
      hand.check_no < (len(players) * 2)):

        hand.check_no = len(players) + 1

    if (hand.check_no >= (len(players) * 2) and
      hand.check_no < (len(players) * 3)):

        hand.check_no = (len(players) * 2) + 1

    if (hand.check_no >= (len(players) * 3) and
      hand.check_no < (len(players) * 4)):

        hand.check_no = (len(players) * 3) + 1

    # Moves the betting on to the next player
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else:
        hand.current_player += 1

    player.player_pot += int(amount)
    hand.player_pot = player.player_pot
    player.chips -= int(amount)
    player.save()
    hand.save()

    return redirect('current_hand', table_id)


# ---- When a player wishes to raise a bet ----
def raise_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)
    amount = request.POST.get('raise', 0)

    # When a player doesn't have enough chips
    if int(amount) > player.chips:
        return HttpResponse('Not enough chips')

    old_player_pot = player.player_pot
    hand.raise_amount += int(amount)
    hand.current_bet += int(amount)
    player.player_pot += (hand.current_bet - player.player_pot)
    hand.player_pot = player.player_pot
    player.chips -= (player.player_pot - old_player_pot)
    player.save()
    hand.pot += (player.player_pot - old_player_pot)

    # The next four if statements reset the check number
    # when a bet is made to work accordingly with the games checking system
    if hand.check_no < len(players):
        hand.check_no = 1

    if (hand.check_no >= len(players) and
      hand.check_no < (len(players) * 2)):

        hand.check_no = len(players) + 1

    if (hand.check_no >= (len(players) * 2) and
      hand.check_no < (len(players) * 3)):

        hand.check_no = (len(players) * 2) + 1

    if (hand.check_no >= (len(players) * 3) and
      hand.check_no < (len(players) * 4)):

        hand.check_no = (len(players) * 3) + 1

    # Moves the betting on to the next player
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else:
        hand.current_player += 1

    hand.save()

    return redirect('current_hand', table_id)


# ------- When a player wishes to call a bet -------
def call_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    player = get_object_or_404(Player, id=player_id)

    # When a player doesn't have enough chips
    if hand.current_bet > player.chips:
        return HttpResponse('Not enough chips')

    if hand.raise_amount != 0:
        hand.raise_amount = hand.current_bet - hand.raise_amount
    else:
        hand.raise_amount = 0

    old_player_pot = player.player_pot
    hand.current_bet -= hand.raise_amount
    player.player_pot = hand.player_pot
    player.chips -= abs(player.player_pot - old_player_pot)
    hand.pot += abs(player.player_pot - old_player_pot)
    hand.check_no += 1

    # If the player is the last player to bet then reset the betting
    if (hand.check_no == len(players) or
      hand.check_no == len(players) * 2 or
      hand.check_no == len(players) * 3 or
      hand.check_no == len(players) * 4):

        hand.current_bet = 0
        hand.raise_amount = 0
        hand.player_pot = 0

    # Moves the betting on to the next player
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else:
        hand.current_player += 1

    hand.save()
    player.save()
    return redirect('current_hand', table_id)


# ------ When a player wishes to check -------
def check_bet(request, table_id, hand_id, player_id):
    players = Player.objects.filter(table_id=table_id)
    hand = get_object_or_404(Hand, id=hand_id)
    hand.check_no += 1

    # Moves the betting on to the next player
    if hand.current_player >= len(players) - 1:
        hand.current_player = 0
    else:
        hand.current_player += 1
    hand.save()
    return redirect('current_hand', table_id)

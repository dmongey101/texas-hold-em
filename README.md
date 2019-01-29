# Texas Holdem
---

Fullstack Frameworks with Django Project - Code Institute

This game is an online mutliplayer texas holdem poker game.
It requires a new user to register and then create or join a table. 
The purpose of the game is not to replicate the normal online poker websites, but rather be a place where friends can get together and play poker no matter where they are in the world.

## How it Works
---

1) Registers or login. 
2) Organise a few friends who will play with you. (2-8 players)
3) Create a table specifying the table name, number of players and the blinds.
4) Join the table.
5) Have your friends register/ login and find the table you created. 
6) Once all the players have joined the cards will be dealt and enjoy the game!

## A live version can be found [Here](https://com-dm-texas-holdem.herokuapp.com/)


# Technologies used

- HTML
 -CSS
- Bootstrap
- Bootswatch
- Python3
- Django2 Framework
- Javascript
- PostgreSQL Database
- Stripe

# Background and features per app
---

## Accounts

The accounts app is used for user authentication. This does not create a player for a game of poker. 
I would like to expand the features on offer to registered users.

### Existing Features
- Users can easily register, log in and log out.
- A user must be logged in to create a table or join a table


### Features left to implement
- Enable a user to view their poker stats i.e games won


## Donations

The donation allows users to make a €5 donation to the sites admin using stripe. This is a temporary feature as the project must be ecommerce.

### Existing Features

- Users can enter address and card information for making purchases.
- Payment processing via stripe.

### Features left to implement
- In the future I will delete this feature and implement stripe connect, 
  where users pay money into a pot when they join a table and the winner recives the pot


## Poker

This is the game of poker runs. This was by far the most challenging app to create. I was told that Django is not made for creating poker games. So I knew what I was getting myself into. 
I'll run you through the steps I took to make it work.

1) I got deck.py and holdem.py files from [omarshammas GitHub](https://github.com/omarshammas/pyPoker-Texas-HoldEm). This helped me create the deck and determine the winner. A made a few changes to these files to be compatible with my code.
2) I then created three models, Table, Player, Hand. The components of these models where changed a lot of over the process of development.
3) I created the template current_hand.html for the gameplay. This file has a lot going on in it as the page has to look different for each player and is differnet for various instances of the game i.e a player can do something only whe its there turn and when to show the flop etc.
4) In the views.py, it was simple enough to get the betting going around the table once. But when a player changes the betting, getting the bet to go back around the table proved to be challenging. How I did it can be seen in the bet and raise functions in poker.views.py
5) Creating the alogrithims for the betting was one of the most challenging parts of this project. Going through all different scenarios of betting and making sure all the totals were being saved correctly in the database was very difficult and time consuming. This is that I ended up with: 
```
# Bet
amount = request.POST['bet']
hand.pot += int(amount)
hand.current_bet += int(amount)
    
# Raise
amount = request.POST['raise']
old_player_pot = player.player_pot
hand.raise_amount += int(amount)
hand.current_bet += int(amount)
player.player_pot += (hand.current_bet - player.player_pot)
hand.player_pot = player.player_pot
player.chips -= (player.player_pot - old_player_pot)
player.save()
hand.pot +=  (player.player_pot - old_player_pot)

# Call
if hand.raise_amount != 0:
    hand.raise_amount = hand.current_bet - hand.raise_amount
else:
    hand.raise_amount = 0
old_player_pot = player.player_pot
hand.current_bet -= hand.raise_amount
player.player_pot = hand.player_pot
player.chips -= (player.player_pot - old_player_pot)
hand.pot += (player.player_pot - old_player_pot)
```





## This project is still in Development 

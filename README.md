# Texas Holdem

Fullstack Frameworks with Django Project - Code Institute

This game is an online mutliplayer texas holdem poker game.
It requires a new user to register and then create or join a table. 
The purpose of the game is not to replicate the normal online poker websites, but rather be a place where friends can get together and play poker no matter where they are in the world.

## How it Works

1) Registers or login. 
2) Organise a few friends who will play with you. (2-8 players)
3) Create a table specifying the table name, number of players and the blinds.
4) Join the table.
5) Have your friends register/ login and find the table you created. 
6) Once all the players have joined the cards will be dealt and enjoy the game!

It was built in Python3 using the Django framework.

## A live version can be found [Here](https://com-dm-texas-holdem.herokuapp.com/)

## UX

The site has a very basic layout, making it easy for a user to interact and navigate around.

* For a first time user, they are given a some brief information about the site 
from the hompage. Then in order to navigate around and use the sites features, they must register an account on the site. 

* When a user is logged in, they can do one of three things:
    1. Donation - They will be presented with a form to fill out, in order to make a donation to the sites creator.
    2. Create Table - Here they fill out a form if they wish to create a table where they and their friends can play.
    3. Find Table - If a users friend has already created a table, then it will appear in the list of current tables. From there they can join the table and begin playing.

* When a user has joined a table, they wait in the lobby until all the players have joined the table. When all players have joined, all users will be redircted to the live game and they can begin playing.

* A user can leave a table at any time. However, they will be unble to rejoin the table.

### Wireframing 

Wireframes were made on pen and paper and can be found in the wireframe folder in the main project file.

## Technologies used

- HTML
 -CSS
- Bootstrap
- Bootswatch
- Python3
- Django2 Framework
- Javascript
- PostgreSQL Database
- Stripe - used for processing payments
- Amazon Web Services (AWS) used to store images for live site

## Features

* Sign-up and login capability
* logout capability
* linkable sections on the site from the navigation bar

### Accounts

The accounts app is used for user authentication. This does not create a player for a game of poker. 
I would like to expand the features on offer to registered users.

#### Existing Features
- Users can easily register, log in and log out.
- A user must be logged in to create a table or join a table


#### Features left to implement
- Enable a user to view their poker stats i.e games won


### Donations

The donation app allows users to make a €5 donation to the sites admin using stripe. This is a temporary feature as the project must be ecommerce.

#### Existing Features

- Users can enter address and card information for making purchases.
- Payment processing via stripe.

#### Features left to implement
- In the future I will delete this feature and implement stripe connect, 
  where users pay money into a pot when they join a table and the winner recives the pot


### Poker

This is where the game of poker runs. This was by far the most challenging app to create. I was told that Django is not made for creating poker games. So I knew what I was getting myself into. 
I'll run you through the steps I took to make it work.

1. I got deck.py and holdem.py files from [omarshammas GitHub](https://github.com/omarshammas/pyPoker-Texas-HoldEm). This helped me create the deck and determine the winner. A made a few changes to these files to be compatible with my code.
2. I then created three models, Table, Player, Hand. The components of these models where changed a lot of over the process of development.
3. I created the template current_hand.html for the gameplay. This file has a lot going on in it as the page has to look different for each player and is differnet for various instances of the game i.e a player can do something only when its there turn and when to show the flop etc.
4. In the views.py, it was simple enough to get the betting going around the table once. But when a player changes the betting, getting the bet to go back around the table proved to be challenging. How I did it can be seen in the bet and raise functions in poker.views.py
5. Creating the alogrithims for the betting was one of the most challenging parts of this project. Going through all different scenarios of betting and making sure all the totals were being saved correctly in the database was very difficult and time consuming. This is what I ended up with: 
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

#### Existing Features

- Users can create a table or join a table
- Users are given 1000 chips to play a game of Texas Hold'em with multiple players
- Users can leave a table at any stage and be redirected back to a list of other live tables

#### Features left to implement

- Refreshing the page after each event in the game to see the outcome is not ideal. I would like to incorporate django channels to the project to make the game real time
- At the moment, there can be no side pots for when a player hasn't enough chips. This is something I will implement in the future 
- I will include a passcode in the Table model so only users who know the passcode may join a table



## Testing 

![alt text](https://travis-ci.org/dmongey101/texas-hold-em.svg?branch=master)

Automated testing was done using Travis-CI. Currently it holds an 86% coverage across the site's three apps. 26 tests were written to achieve this.

To run the tests, when you have the project running locally, enter:

```
$ python3 manage.py test
```
To run the tests you need to remove the DATABASE_URL environment variable.
You can remove the env variable using:
```
$ unset DATABASE_URL
```

The site was tested on 21" monitors, 15" and 13" laptop screens and on an iPhone SE and iPhone 8 screen to test responsiveness.
It was also tested using chrome, firefox and safari.

Manual tests were also done to ensure links/form submissions/model relationships/donations worked correctly and that the site was defensively designed.

Manual testing was done to ensure:

* The site works as intended.
* Logging in and out and registering works as intended.
* Correct rules of Texas Hold'em apply
* Players chips and the table pot values are handled correctly for each action

## Deployment

The site is hosted on heroku.

Static assets are hosted on Amazon S3.

### Run Locally

1. Clone the [github repository](https://github.com/dmongey101/texas-hold-em)
2. Install requirements:
```
$ pip3 install -r requirements.txt
```
3. In base.py set debug to True.
4. Get a secret key and set it as an environment variable. You can get one at https://www.miniwebtool.com/django-secret-key-generator/
5. Set as an environment variable DJANGO_SETTINGS_MODULE equal to 'poker_project.settings.dev':
6. Migrate:
```
$ python3 manage.py migrate
```
7. Create a superuser:
```
$ python3 manage.py createsuperuser
```
8. Update your allowed hosts in base.py.
9. The site will now run locally.

## Credits

### Content

* Theme was taken from https://bootswatch.com/

### Media

* Card images came from https://codewithchris.com/
* Poker chip image came from https://www.freeiconspng.com/img/43958
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

## Testing the Features 

To test the features of the app: 
1) Open two browsers (or one regular and one Incognito Chrome window).
2) Visit https://com-dm-texas-holdem.herokuapp.com/ on both browsers and sign up with two seperate accounts, or, two users have been        created for testing so feel free to use them.
    * Account 1
        - **username**: Harry
        - **password**: p@ssword123
    * Account 2
        - **username**: Simon
        - **password**: p@ssword123
3) As this game doesn't respond to live events, please **refresh the page** when changing from one browser to the other, to deal with the    games progression. 
4) When logged in, use Harry to create a table. Fill out the form ensuring number of players = 2 and blinds = 10.
5) Let Harry join that table and then switch to Simon. As Simon, find the table created by Harry and join it.
6) As Harry joined the table first, he is first dealer. Simon is small blind. As there are only two players, big blind goes back to         Harry. 
7) Let Simon call as his first turn. By calling he is matching the big blind. 
8) On Harrys account (remember to refresh), as he is big blind, and it is pre flop, he will have the oppurtunity to raise or check. Let     Harry check.
9) The Flop cards should appear on both screens. Small blind always starts the betting so switch over to Simon

**Testing Checking:**

10) Let Simon Check. Betting should move to Harry where he can bet, check or fold.
11) Let Harry Check. This will end Flop betting and the Turn card will show.

**Testing Betting:**

11) Let Simon Bet 10. The pot should increase by 10 and Simons chips decrease by 10. 

**Testing Calling:**

12) Let Harry Call. The pot should increase by 10 and Harrys chips decrease by 10. This will end Turn betting and the River card will        show.

**Testing Raising:**

13) Let Simon Bet 10.
14) Let Harry Raise 10. The pot should increase by 20 and Harrys chips decrease by 20.

**Testing Winner:**

15) Let Simon Call. This will end the hand.
16) A winner will have been determined and that player should recieve the pot.

**Testing Dealing:**

17) A deal button should now appear on Simons page as he is now the dealer. Press the button and a new set of cards will be dealt to all     players.
18) The blinds will also be taken from the appropriate players chip stack. 

**Testing Folding:**

19) Let Harry Raise 10.
20) Let Simon Fold.
21) As there are only two players, Harry wins the hand. When there are more than 2 players the betting would continue to the next player,     and the player that folded will be skipped until the next hand.

**Testing for when player has no chips:**

22) Let Harry deal the cards.
23) Let Simon Call.
24) Let Harry Check.

**If Simon has more chips than Harry:**
25) Let Simon Bet the total amount of his chips.
26) Let Harry Call.
    
**If Harry has more chips than Simon:**
25) Let Simon Check.
26) Let Harry Bet the total amount of his chips.
27) Let Simon Call.


28) Let Simon Check.
29) Let Harry Check.
30) Let Simon Check.
31) Let Harry Check.
32) The loser of the hand will be deleted from the game.
33) The game is now over.

**Testing Leaving:**

33. Let the remaining player leave the game by pressing the leave button on the top left of the screen.
34. The user will be redirected to the view table page(this will not be seen by the user), where the table will be deleted as there are      no more players. They will then be redirected to the find table page.

## UX

The site has a very basic layout, making it easy for a user to interact and navigate around. The game is intended to be used to play poker as quick and easy as possible, which the site allows the user to do. 

* For a first time user, they are given a some brief information about the site 
  from the hompage. Then in order to navigate around and use the sites features, they must register an account on the site. 

* When a user is logged in, they can do one of three things:
    1. Donation - They will be presented with a form to fill out, in order to make a donation to the sites creator.
    2. Create Table - Here they fill out a form if they wish to create a table where they and their friends can play.
    3. Find Table - If a users friend has already created a table, then it will appear in the list of current tables. From there they can join the table and begin playing.

* When a user has joined a table, they wait in the lobby until all the players have joined the table. When all players have joined, all    users will be redircted to the live game and they can begin playing.

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

This is where the game of poker runs. This was by far the most challenging app to create. 
I'll run you through the steps I took to make it work.

1. I got deck.py and holdem.py files from [omarshammas GitHub](https://github.com/omarshammas/pyPoker-Texas-HoldEm). This helped me         create the deck and determine the winner. A made a few changes to these files to be compatible with my code.
2. I then created three models, Table, Player and Hand. The components of these models where changed a lot of over the process of           development. The models are crucial to the flow of the game. Whenever a User joins a Table a Player is created. A Player is given a      seat number on a Table and is unique to one particular Table. When a Player leaves a Table the Player is deleted from the database.
   A Player is dealt two Card objects at the start of every Hand and are saved as strings in the database. When neccesary, the cards will be changed back to objects. 
   The Hand model is asscociated to one Table. Like the Player model, the Hand is dealt five Card objects, saved as strings. A Hand has two many to many relationship with Player, one for a list of all Players in a Hand, and one for a list of winners in a Hand. The six IntegerField's in the Hand model were carefully selected to handle the betting. These fields and the betting alogrithim in views.py are what make up the most difficult part of the app, the betting. 
3. I created the template current_hand.html for the gameplay. This file has a lot going on in it as the page has to look different for      each player and is differnet for various instances of the game i.e a player can do something only when its there turn and when to show    the flop etc.
4. In the views.py, it was simple enough to get the betting going around the table once. But when a player changes the betting, getting     the bet to go back around the table proved to be challenging. How I did it can be seen in the bet and raise functions in                 poker.views.py
5. Creating the alogrithims for the betting was one of the most challenging parts of this project. Going through all different scenarios    of betting and making sure all the totals were being saved correctly in the database was very difficult and time consuming. This is      what I ended up with: 
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
6. I wanted to make the game as automated as I possibly could. So added a few features to do this.
    * When all players have joined a table, the will be redirected to the table and the cards will be dealt. So two things happen there.   When the last player joins, they redirect to the deal card function which will deal all the players cards. And all the other         players who have joined will be redirected to the current hand function.
    * Usually when a player leaves a table they will be redirected to the find table page. But if they are the last player on the table,   when they leave they will be redirected to the view table page. The Table model will be then be deleted and then the User will be    redirected to find table. This will be a smooth process for the User as it appears to them as if they were redirected straight from   the current hand to the find table page.

7. I then added blinds to the game which made everything a bit more difficult. I wanted the game to be as close to a real game of Texas     Hold'em as possible. So betting always starts with small blind. A player leaving the game messed up the the order of the blinds.
   Trying to deal with this proved to be very difficult and required a lot of testing for different secenarios.
   The finished algorithim looked like this:
   ```
   table.dealer += 1  # First dealer will be player 0
    table.small_blind += 1
    table.big_blind += 1

    # Moves on positions where there are empty seats
    player_seats = []
    for player in players:
        player_seats.append(player.seat_num)

    if table.dealer > sorted(player_seats)[-1]:
        table.dealer = 0
    while table.dealer not in player_seats:
        table.dealer += 1

    if table.small_blind > sorted(player_seats)[-1]:
        table.small_blind = 0
    while table.small_blind not in player_seats:
        table.small_blind += 1

    if table.big_blind > sorted(player_seats)[-1]:
        table.big_blind = 0
    while table.big_blind not in player_seats:
        table.big_blind += 1

    table.save()
    ```

Testing this app to ensure all the features worked properly was long and awkward. The number of players in a game represented the number of browsers I had open. I tried to test every secenario for two player games, all the way up to five player games.

#### Existing Features

- Users can create a table or join a table
- Users are given 1000 chips to play a game of Texas Hold'em with multiple players
- Users can leave a table at any stage and be redirected back to a list of other live tables

#### Features left to implement

- Refreshing the page after each event in the game to see the outcome is not ideal. I would like to incorporate django channels to the     project to make the game real time
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

## Issues

Due to time contraints, there were a few issues left unresolved.

1) The main issue is the game isn't real time. Having to refresh the page to see updates is not ideal. Trying to implement this in the      time frame I had would have been very difficult. I will however implement this feature in the near future using django channels.
2) The poker.views.py file is very long and a lot of the code is probaly unneccesary. My main focus was to get the gamne to work.
3) I would also like to go back and re-style the whole current_hand.html file, to make it look more appealing and fun for the user to       play.
4) At the moment there is no side pot feature for then a player has to few chips to match other players betting. Thus the game off being    like a real game of Texas Hold'em. 

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

* Navbar idea came from https://www.zynga.com/
* Navbar and sidenav css and js came from https://materializecss.com/

### Media

* Font awesome was used for the various icons in the site.
* Google fonts used
* Card images came from https://codewithchris.com/
* Poker chip image and icon came from https://www.flaticon.com/
* All mp3 files came from https://www.zapsplat.com/
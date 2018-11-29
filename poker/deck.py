from random import shuffle


class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value
    
    @staticmethod
    def from_str(str):
        if str == "AD":
            return Card(0, 14)
        elif str == "AH":
            return Card(1, 14)
        elif str == "AS":
            return Card(2, 14)
        elif str == "AC":
            return Card(3, 14)
        elif str == "KD":
            return Card(0, 13)
        elif str == "KH":
            return Card(1, 13)
        elif str == "KS":
            return Card(2, 13)
        elif str == "KC":
            return Card(3, 13)
        elif str == "QD":
            return Card(0, 12)
        elif str == "QH":
            return Card(1, 12)
        elif str == "QS":
            return Card(2, 12)
        elif str == "QC":
            return Card(3, 12)
        elif str == "JD":
            return Card(0, 11)
        elif str == "JH":
            return Card(1, 11)
        elif str == "JS":
            return Card(2, 11)
        elif str == "JC":
            return Card(3, 11)
        elif str == "10D":
            return Card(0, 10)
        elif str == "10H":
            return Card(1, 10)
        elif str == "10S":
            return Card(2, 10)
        elif str == "10C":
            return Card(3, 10)
        elif str == "9D":
            return Card(0, 9)
        elif str == "9H":
            return Card(1, 9)
        elif str == "9S":
            return Card(2, 9)
        elif str == "9C":
            return Card(3, 9)
        elif str == "8D":
            return Card(0, 8)
        elif str == "8H":
            return Card(1, 8)
        elif str == "8S":
            return Card(2, 8)
        elif str == "8C":
            return Card(3, 8)
        elif str == "7D":
            return Card(0, 7)
        elif str == "7H":
            return Card(1, 7)
        elif str == "7S":
            return Card(2, 7)
        elif str == "7C":
            return Card(3, 7)
        elif str == "6D":
            return Card(0, 6)
        elif str == "6H":
            return Card(1, 6)
        elif str == "6S":
            return Card(2, 6)
        elif str == "6C":
            return Card(3, 6)
        elif str == "5D":
            return Card(0, 5)
        elif str == "5H":
            return Card(1, 5)
        elif str == "5S":
            return Card(2, 5)
        elif str == "5C":
            return Card(3, 5)
        elif str == "4D":
            return Card(0, 4)
        elif str == "4H":
            return Card(1, 4)
        elif str == "4S":
            return Card(2, 4)
        elif str == "4C":
            return Card(3, 4)
        elif str == "3D":
            return Card(0, 3)
        elif str == "3H":
            return Card(1, 3)
        elif str == "3S":
            return Card(2, 3)
        elif str == "3C":
            return Card(3, 3)
        elif str == "2D":
            return Card(0, 2)
        elif str == "2H":
            return Card(1, 2)
        elif str == "2S":
            return Card(2, 2)
        else:
            return Card(3, 2)
    
    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        text = ""
        if self.value < 0:
            return "Joker";
        elif self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)
        

        if self.symbol == 0:    #D-Diamonds
            text += "D" 
        elif self.symbol == 1:  #H-Hearts
            text += "H"
        elif self.symbol == 2:  #S-Spade
            text += "S"
        else:   #C-Clubs
            text += "C" 
            
        return text    
        
        
    
        
    
class deck:
    
    #Initializes the deck, and adds jokers if specified
    def __init__(self, addJokers = False):
        self.cards = []
        self.inplay = []
        self.addJokers = addJokers
        for symbol in range(0,4):
            for value in range (2,15):
                self.cards.append( Card(symbol, value) )
        if addJokers:
            self.total_cards = 54
            self.cards.append( Card(-1, -1) )
            self.cards.append( Card(-1, -1) )
        else:
            self.total_cards = 52

    #Shuffles the deck
    def shuffle(self):
        self.cards.extend( self.inplay )
        self.inplay = []
        shuffle( self.cards )
    
    #Cuts the deck by the amount specified
    #Returns true if the deck was cut successfully and false otherwise
    def cut(self, amount):
        if not amount or amount < 0 or amount >= len(self.cards):
            return False #returns false if cutting by a negative number or more cards than in the deck
        
        temp = [] 
        for i in range(0,amount):
            temp.append( self.cards.pop(0) )
        self.cards.extend(temp)
        return True

    #Returns a data dictionary 
    def deal(self, number_of_cards):
        
        if(number_of_cards > len(self.cards) ):
            return False #Returns false if there are insufficient cards
        
        inplay = []
        for i in range(0, number_of_cards):
            inplay.append( self.cards.pop(0) )
        
        self.inplay.extend(inplay)            
        return inplay      
    
    def cards_left(self):
        return len(self.cards)
        

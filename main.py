
import random
import threading
import socket 
from PIL import Image
from tkinter import *
from PIL import ImageTk, Image
# constants

#root = Tk()
#root.geometry("1000x1000")

#card constants
COLOURS = ["yellow"]#,"red","green","blue"]
TYPES = ["1","2","3","4","5","6","7","8","9","skip","+2","reverse","1","2","3","4","5","6","7","8","9","skip","+2","reverse","0"]
SPECIAL = ["+4","wild","+4","wild","+4","wild","+4","wild"]

# game variables 

cardsPerHand = 7
players = []
discardPile = []

# ----- classes -----

class card :
    
    def __init__(self,id,type,colour):
        self.id = id
        self.colour = str(colour)
        self.type = str(type)
        self.name = str(self.colour + " " + self.type)
        self.root = str("assets\\" + self.colour + "_" + self.type + ".png")
        self.img = ImageTk.PhotoImage(Image.open(self.root))
    
    def createLable(self,master):
        self.lable = Label(master, image = self.img)

class player :
    def __init__(self):
        self.hand = []
    def pickUp(self) :
        global deck
        self.hand.append(deck[0])
        deck.pop(0)
    def playCard(self,cardID) :
        global discardPile
        #looks for card and then places it in the discard pile
        for index,card in enumerate(self.hand) :
            if cardID == card.id : 
                self.hand.pop(index)
                discardPile.insert(0,card)

# -------- game functions --------

def gen_deck() :
    # genorate deck list
    deck = []
    idCounter = 0
    for colour in COLOURS :
        for type in TYPES :

            deck.append(card(idCounter,type,colour))
            idCounter += 1
    for special in SPECIAL :
        deck.append(card(idCounter,special,""))
        idCounter += 1
    #shuffle deck
    random.shuffle(deck)
    #return deck
    return deck

def handOutCards() :
    for x in range(cardsPerHand) :
        for person in players :
            person.pickUp()

def displayHand(player) :
    print("player ",players.index(player),":")
    for card in player.hand :
        print("",card.colour,card.type,"ID: ",card.id,",",end="")
    print("")

def displayDiscardPile() :
    global deck
    print("discard pile : ",end="")
    for cards in discardPile :
        print("",cards.colour,cards.type,"ID: ",cards.id,",",end="")
        print()

def canPlace(card) :
    global discardPile
    deckCard = discardPile[0]
    print("deck card : {}{} \n player card : {}{}".format(deckCard.colour,deckCard.type,card.colour,card.type))
    print("same type is",deckCard.type == card.type , ", same colour is",deckCard.colour == card.colour)
    if deckCard.type == card.type or deckCard.colour == card.colour :
        return True
    else : 
        return False

def turn(player) :
    player  = players[player]

    turnTaken = False
    while turnTaken == False :
        displayDiscardPile()
        cardChoiceId = int(input("card id >> "))
        # check if choice is pick up
        if cardChoiceId == -1 :
            player.pickUp()
            turnTaken = True
        else :
            #find chosen card in deck and check if can be played
            for card in player.hand :
                if card.id == cardChoiceId :
                    print("card found")
                if card.id == cardChoiceId and canPlace(card):
                    player.playCard(card.id)
                    turnTaken = True
        if turnTaken == False :   
            print("card not found or cant be placed")
    displayHand(player)
    displayDiscardPile()

def setup() :
    #genorates deck
    deck = gen_deck()
    #hands ou cards
    handOutCards()
    #displays each persons hand
    for user in players :
        displayHand(user)
    #take card from deck and put in discard pile
    discardPile.append(deck[0])
    deck.pop(0)

# ----- window functions ------

def host() :
    Host = socket.gethostname()2
    binded = False
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while  binded == False :
        port = random.randint(49152,65535)
        try :
            server.bind((Host,port))
        except :
            



def join() :



# ----- connection functions -------

def identifyUser() :
    usertype = str(input("join or host j/h >> ")) 
    if usertype == "j" :
        print("join")
    elif usertype == "h" :
        print("host")
    else :
        print("invalid choice please choose again")
        identifyUser()

# ----- establish connection code ------

identifyUser()

# ----- temp code ----

for person in range(int(input("number of players"))) :
    players.append(player())

# ------ setup ------

setup()

# ---- game play ----

turnPointer = 0

turn(0)
import random
import threading
import socket 
from PIL import Image
from tkinter import *
from PIL import ImageTk, Image
import time
import pickle
from classes import *
# constants

#root = Tk()
#root.geometry("1000x1000")

#card constants
COLOURS = ["yellow"]#,"red","green","blue"]
TYPES = ["1","2","3","4","5","6","7","8","9","skip","+2","reverse","1","2","3","4","5","6","7","8","9","skip","+2","reverse","0"]
SPECIAL = ["+4","wild","+4","wild","+4","wild","+4","wild"]

#connection constants

MSG_ORDER = {0:"hand",1:"numOfCardPerPlayer",2:"playerNum",3:"discardTopCard"}



# game variables 

cardsPerHand = 7

# ----- classes -----

class player :
    def __init__(self,conn,addr,nickname):
        self.conn = conn
        self.addr = addr
        self.name = nickname
        self.hand = []

    def pickUp(self) :
        global gameVar
        self.hand.append(gameVar.deck[0])
        gameVar.deck.pop(0)
    
    def playCard(self,cardID) :
        global gameVar
        #looks for card and then places it in the discard pile
        for index,card in enumerate(self.hand) :
            if cardID == card.id : 
                self.hand.pop(index)
                gameVar.discardPile.insert(0,card)

gameVar = game()

# -------- game functions --------

def gen_deck() :
    # genorate deck list
    print("genorating deck")
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
    global gameVar
    print("handing out cards")
    for x in range(cardsPerHand) :
        for person in gameVar.players :
            person.pickUp()
            time.sleep(0.1)

def displayHand(player) :
    global gameVar
    print("player ",gameVar.players.index(player),":")
    for card in player.hand :
        print("",card.colour,card.type,"ID: ",card.id,",",end="")
    print("")

def displayDiscardPile() :
    print("discard pile : ",end="")
    for cards in gameVar.discardPile :
        print("",cards.colour,cards.type,"ID: ",cards.id,",",end="")
        print()

def canPlace(card) :
    global gameVar
    deckCard = gameVar.discardPile[0]
    print("deck card : {}{} \n player card : {}{}".format(deckCard.colour,deckCard.type,card.colour,card.type))
    print("same type is",deckCard.type == card.type , ", same colour is",deckCard.colour == card.colour)
    if deckCard.type == card.type or deckCard.colour == card.colour :
        return True
    else : 
        return False

def turn(player) :
    player  = gameVar.players[player]
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

def gameStart() :
    print("game starting")
    time.sleep(2)
    #makes game variables class
    #genorates deck
    gameVar.deck = gen_deck()
    #hands ou cards
    handOutCards()
    #displays each persons hand
    for user in gameVar.players :
        displayHand(user)
    #take card from deck and put in discard pile
    gameVar.discardPile.append(gameVar.deck[0])
    gameVar.deck.pop(0)

def gameSetup() : 
    global gameVar
    gameVar = game()
# ----- conection functions ------

def host() :
    Host = socket.gethostname()
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = random.randint(49152,65535)
    try :
        server.bind((Host,port))
    except :
        print("finding port")
        host()
    print("binded server to {}:{}".format(Host,port))
    global gameVar
    #while len(players) == 0 :
    print("listening")
    print(len(gameVar.players),gameVar.players)
    server.listen(2)
    conn , addr = server.accept()
    print("connected by", addr)
    tread = threading.Thread(target=handleClient,args=(conn,addr))
    tread.start()
    gameStart()

def join() :
    serverAdress = str(input("join id :"))
    name = str(input("name : "))
    for index,char in enumerate(serverAdress) :
        if char == ":" :
            Host = serverAdress[0:index]
            port = serverAdress[index + 1:]
            break
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        connection.connect((Host,int(port)))
    except:
        print("cant connect please try again")
        join()
    print("connected")
    sendMsg(name,connection)
    while True:
        data = reciveMsg(connection)
        for card in data :
            print(card.colour,card.type,card.id,end=" , ")
        print("")


def handleClient(conn,addr):
    global gameVar
    nick = reciveMsg(conn)
    gameVar.players.append(player(conn,addr,nick))
    print(gameVar.players)
    print("user:",nick,"joined")
    while True:
        for num,client in enumerate(gameVar.players) :
            if client.name == nick :
                displayHand(client)
                msg = [client.hand,]
                time.sleep(0.2)
                sendMsg(msg,conn)

def sendMsg(messsage,conn):
    global card
    print("pickle, ",messsage)
    messsage = pickle.dumps(messsage)
    conn.sendall(messsage)

def reciveMsg(conn) :
    msg = conn.recv(1024)
    return pickle.loads(msg) 
 
def identifyUser() :
    usertype = str(input("join or host j/h >> ")) 
    if usertype == "j" :
        print("join")
        join()
    elif usertype == "h" :
        print("host")
        host()
    else :
        print("invalid choice please choose again")
        identifyUser()

# ----- establish connection code ------
gameSetup()
identifyUser()
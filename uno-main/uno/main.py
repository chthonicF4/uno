import random
import threading
import socket 
from tkinter import *
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
    if deckCard.type == card.type or deckCard.colour == card.colour or card.colour == "":
        return True
    else : 
        return False

def turn(player) :
    user  = gameVar.players[player]
    turnTaken = False
    while turnTaken == False :
        displayDiscardPile()
        cardChoiceId = str
        while cardChoiceId == False :
            cardChoiceId = reciveMsg(user.conn)
        # check if choice is pick up
        if cardChoiceId == -1 :
            user.pickUp()
            turnTaken = True
        else :
            #find chosen card in deck and check if can be played
            for card in user.hand :
                if card.id == cardChoiceId and canPlace(card):
                    user.playCard(card.id)
                    turnTaken = True
        if turnTaken == False :   
            print("card not found or cant be placed")
            turn(player)

def gameStart() :
    global gameVar
    print("game starting")
    gameVar.gameStart = True
    time.sleep(2)
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
    # start cycling through turns
    while anyoneHas0Cards() == False :
        turn(gameVar.turn)
        gameVar.turn += 1
        if gameVar.turn > len(gameVar.players) :
            gameVar = 0 
        
def anyoneHas0Cards():
    for person in gameVar.players :
        if len(person.hand) == 0 :
            return True

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
        print("finding port...")
        host()
    print("binded server to {}:{}".format(Host,port))
    play = threading.Thread(target=join,args=(Host,port))
    play.start()
    global gameVar
    while len(gameVar.players) <= 1 :
        print("listening")
        print(len(gameVar.players),gameVar.players)
        server.listen(2)
        conn , addr = server.accept()
        print("connected by", addr)
        # make thread for new player
        clientThread = threading.Thread(target=handleClient,args=(conn,addr))
        clientThread.start()
        time.sleep(0.1)
    gameStart()

def join(Host="",port="") :
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
    name = str(input("name : "))
    if Host != "" and port != "" :
        pass
    else :
        serverAdress = str(input("join id :"))
        for index,char in enumerate(serverAdress) :
            if char == ":" :
                Host = serverAdress[0:index]
                port = serverAdress[index + 1:]
                break
    try:
        connection.connect((Host,int(port)))
    except:
        print("cant connect please try again")
        join()
    print("connected")
    sendMsg(name,connection)
    while True:
        data = reciveMsg(connection)
        print(data)



def handleClient(conn,addr):
    global gameVar
    nick = reciveMsg(conn)
    gameVar.players.append(player(conn,addr,nick))
    print("user:",nick,"joined")
    while gameVar.gameStart == False :
        pass
    while True:
        for num,client in enumerate(gameVar.players) :
            if client.name == nick :
                msg = constructMsg(num,client)
                time.sleep(0.2)
                sendMsg(msg,conn)

def sendMsg(messsage,conn):
    global card
    messsage = pickle.dumps(messsage)
    conn.sendall(messsage)

def reciveMsg(conn) :
    msg = conn.recv(1024)
    return pickle.loads(msg) 
 
def identifyUser() :
    usertype = str(input("join or host j/h >> ")) 
    if usertype == "j" :
        join()
    elif usertype == "h" :
        host()
    else :
        print("invalid choice please choose again")
        identifyUser()

def constructMsg(num,client):
    #     order of data : is turn of player (bool) , player hand (list) , each players card count () , top card on discard pile . 
    try:
        topCard = gameVar.discardPile[0]
    except:
        topCard = ""
    msg = [ (num == gameVar.turn) , client.hand , gameVar.numOfCardPerPlayer() , topCard ]
    return  msg

# ----- establish connection code ------
gameSetup()
identifyUser()
from tkinter import *
from PIL import ImageTk, Image


class card :
    
    def __init__(self,id,type,colour):
        self.id = id
        self.colour = str(colour)
        self.type = str(type)
        self.name = str(self.colour + " " + self.type)
        self.root = str("assets\\" + self.colour + "_" + self.type + ".png")
        #self.img = ImageTk.PhotoImage(Image.open(self.root))
    
    def createLable(self,master):
        self.lable = Label(master, image = self.img)


class game :
    def __init__(self):
        self.deck = []
        self.players = []
        self.discardPile = []
        self.turn = 0
        self.gameStart = False
    
    def numOfCardPerPlayer(self) :
        out = []
        for player in self.players :
            try :
                out.append(len(player.hand))
            except :
                out.append(0)
            return out

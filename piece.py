#All the classes for pieces
#Simply describes how they are drawn
from vpython import*
import numpy as np
import fvector as fvec
class Piece:
    'A parent class for all the piece subclasses'
    def __init__(self):
        self.base = None
        self.ogcolor = None
        self.boxes = []

    def move(self,newPos):
        self.base.pos = newPos
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)
        self.base.color = self.ogcolor
        self.started=True
        return True
        

    def __eq__(self, obj):
        if(obj!=None):
            return self.base.pos.equals(obj.pos)


    def setvisible(self,state):
        'Makes more complex shapes invisible'
        if hasattr(self.base,'objects'):
            for obj in self.base.objects:
                obj.visible = state
        else:
            self.base.visible = state

    def select(self):
        self.selected = not self.selected

    def completepositions(self,x,y,z,d,kingpos,board):
        nowvec = fvec.Fvector(x,y,z,d)
        return nowvec.removecheckpos(self,board,kingpos)

    def glowlegal(self,kingpos,board):
        x = round(self.base.pos.x)
        y = round(ytoy(self.base.pos.y))
        z = round(ztoz(self.base.pos.z))
        d = round(ztod(self.base.pos.z))
        positions = self.completepositions(x,y,z,d,kingpos,board)

        for boxx in positions:
            self.boxes.append(box(pos=vec(boxx.x,(boxx.y*2.5),boxx.z+(5*boxx.d)),length=1,height=0.1,width=1,color=color.green))

    def unglow(self):
        for boxx in self.boxes:
            x = round(boxx.pos.x)
            y = round(ytoy(boxx.pos.y))
            z = round(ztoz(boxx.pos.z))
            d = round(ztod(boxx.pos.z))
            sColor=None
            if (x+y+z+d) % 2 == 1:
                sColor = color.blue
            else: 
                sColor = color.white
            box(pos=vector(x,(y*2.5),z+(5*d)),length=1,height=0.1,width=1,color=sColor)
        self.boxes.clear()

    def getpos(self):
        x = round(self.base.pos.x)
        y = round(ytoy(self.base.pos.y))
        z = round(ztoz(self.base.pos.z))
        d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(x,y,z,d)
        return self.posvec

class Pawn(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 1
        self.started=False
        self.selected = False
        #self.base = compound([cone(pos=(spos),radius=0.4,axis=vector(0,1,0),color=sColor),
        #sphere(pos=(spos)+vector(0,1,0),radius=0.1,axis=vector(0,1,0),color=sColor)])
        self.base = cone(pos=(spos),radius=0.4,axis=vector(0,1,0),color=sColor)
        self.ogcolor = sColor
        self.boxes = []
        self.positions = None
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)

    def __repr__(self):
        return 'p'

    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        c = -1
        if(self.ogcolor.equals(color.white)):
            c = 1
        self.positions = None
        positions = self.posvec.pawn(0,0,c,0,True,board)
        if(not self.started):
            positions+=self.posvec.pawn(0,0,c,0,False,board)
        positions+=self.posvec.pawn(1,0,c,0,True,board)
        positions+=self.posvec.pawn(-1,0,c,0,True,board)
        positions+=self.posvec.pawn(0,1,c,0,True,board)
        positions+=self.posvec.pawn(0,-1,c,0,True,board)
        positions+=self.posvec.pawn(0,0,c,c,True,board)
        self.positions = positions
        return positions
        

class Rook(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 5
        self.started=False
        self.selected = False
        self.ogcolor = sColor
        self.boxes = []
        self.base = compound([cylinder(pos=spos+vector(0,0,0),radius=0.3,length=0.8,axis=vector(0,1,0),color=sColor),cylinder(pos=spos+vector(0,0.8,0),length=0.2,radius=0.4,axis=vector(0,1,0),color=sColor)])
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)

    def __repr__(self):
        return 'r'
        
    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        positions = self.posvec.getPosArray(1,0,0,0,False,board)
        positions+= self.posvec.getPosArray(-1,0,0,0,False,board)
        positions+= self.posvec.getPosArray(0,1,0,0,False,board)
        positions+= self.posvec.getPosArray(0,-1,0,0,False,board)
        positions+= self.posvec.getPosArray(0,0,1,0,False,board)
        positions+= self.posvec.getPosArray(0,0,-1,0,False,board)
        positions+= self.posvec.getPosArray(0,0,0,1,False,board)
        positions+= self.posvec.getPosArray(0,0,0,-1,False,board)
        self.positions = positions
        return positions

class Knight(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 3
        self.started=False
        self.selected = False
        self.ogcolor = sColor
        self.boxes = []
        face = 0.1
        if(sColor == color.red):
            face = -0.1
        self.base = compound([box(pos=spos+(vector(0,0.4,0)),width=0.4,length=0.8,height=0.4,axis=vector(0,1,0),color=sColor),
        box(pos=spos+(vector(0,0.8,face)),width=0.6,length=0.4,height=0.4,axis=vector(0,1,0),color=sColor)])
        #cone(pos=spos+vector(0,0.6,0),radius=0.2,axis=vector(0,0,face),color=sColor)])
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)


    def __repr__(self):
        return 'k'

    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        positions = self.posvec.getPosArray(2, 1, 0, 0, True,board)
        positions+= self.posvec.getPosArray(2, 0, 1, 0, True,board)
        positions+= self.posvec.getPosArray(2, 0, 0, 1, True,board)
        positions+= self.posvec.getPosArray(1, 2, 0, 0, True,board)
        positions+= self.posvec.getPosArray(0, 2, 1, 0, True,board)
        positions+= self.posvec.getPosArray(0, 2, 0, 1, True,board)
        positions+= self.posvec.getPosArray(1, 0, 2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 1, 2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 0, 2, 1, True,board)
        positions+= self.posvec.getPosArray(1, 0, 0, 2, True,board)
        positions+= self.posvec.getPosArray(0, 1, 0, 2, True,board)
        positions+= self.posvec.getPosArray(0, 0, 1, 2, True,board)

        positions+= self.posvec.getPosArray(-2, 1, 0, 0, True,board)
        positions+= self.posvec.getPosArray(-2, 0, 1, 0, True,board)
        positions+= self.posvec.getPosArray(-2, 0, 0, 1, True,board)
        positions+= self.posvec.getPosArray(1, -2, 0, 0, True,board)
        positions+= self.posvec.getPosArray(0, -2, 1, 0, True,board)
        positions+= self.posvec.getPosArray(0, -2, 0, 1, True,board)
        positions+= self.posvec.getPosArray(1, 0, -2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 1, -2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 0, -2, 1, True,board)
        positions+= self.posvec.getPosArray(1, 0, 0, -2, True,board)
        positions+= self.posvec.getPosArray(0, 1, 0, -2, True,board)
        positions+= self.posvec.getPosArray(0, 0, 1, -2, True,board)

        positions+= self.posvec.getPosArray(2, -1, 0, 0, True,board)
        positions+= self.posvec.getPosArray(2, 0, -1, 0, True,board)
        positions+= self.posvec.getPosArray(2, 0, 0, -1, True,board)
        positions+= self.posvec.getPosArray(-1, 2, 0, 0, True,board)
        positions+= self.posvec.getPosArray(0, 2, -1, 0, True,board)
        positions+= self.posvec.getPosArray(0, 2, 0, -1, True,board)
        positions+= self.posvec.getPosArray(-1, 0, 2, 0, True,board)
        positions+= self.posvec.getPosArray(0, -1, 2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 0, 2, -1, True,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, 2, True,board)
        positions+= self.posvec.getPosArray(0, -1, 0, 2, True,board)
        positions+= self.posvec.getPosArray(0, 0, -1, 2, True,board)

        positions+= self.posvec.getPosArray(-2, -1, 0, 0, True,board)
        positions+= self.posvec.getPosArray(-2, 0, -1, 0, True,board)
        positions+= self.posvec.getPosArray(-2, 0, 0, -1, True,board)
        positions+= self.posvec.getPosArray(-1, -2, 0, 0, True,board)
        positions+= self.posvec.getPosArray(0, -2, -1, 0, True,board)
        positions+= self.posvec.getPosArray(0, -2, 0, -1, True,board)
        positions+= self.posvec.getPosArray(-1, 0, -2, 0, True,board)
        positions+= self.posvec.getPosArray(0, -1, -2, 0, True,board)
        positions+= self.posvec.getPosArray(0, 0, -2, -1, True,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, -2, True,board)
        positions+= self.posvec.getPosArray(0, -1, 0, -2, True,board)
        positions+= self.posvec.getPosArray(0, 0, -1, -2, True,board)
        self.positions = positions
        return positions

    

class Bishop(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 3
        self.started=False
        self.selected = False
        self.ogcolor = sColor
        self.boxes = []
        self.base = compound([cylinder(pos=spos+vector(0,0,0),radius=0.2,length=0.8,axis=vector(0,1,0),color=sColor),cone(pos=spos+vector(0,0.8,0),radius=0.2,axis=vector(0,1,0),color=sColor)])
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)



    def __repr__(self):
        return 'b'
    
    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        positions = self.posvec.getPosArray(1,1,0,0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 1, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 1, 1, 0,False,board)
        positions+= self.posvec.getPosArray(0, 1, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 0, 1, 1,False,board)

        positions+= self.posvec.getPosArray(-1, 1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 1, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, -1, 1, 0,False,board)
        positions+= self.posvec.getPosArray(0, -1, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 0, -1, 1,False,board)

        positions+= self.posvec.getPosArray(1, -1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, -1, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 1, -1, 0,False,board)
        positions+= self.posvec.getPosArray(0, 1, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 0, 1, -1,False,board)

        positions+= self.posvec.getPosArray(-1, -1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, -1, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, -1, -1, 0,False,board)
        positions+= self.posvec.getPosArray(0, -1, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 0, -1, -1,False,board)
        self.positions = positions
        return positions
        
class Queen(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 9
        self.started=False
        self.selected = False
        self.ogcolor = sColor
        self.boxes = []
        self.base = compound([cylinder(pos=spos+vector(0,0,0),radius=0.4,length=1.0,axis=vector(0,1,0),color=sColor),sphere(radius=0.4,pos=spos+vector(0,1.4,0),color=sColor)])
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)
    
    def __repr__(self):
        return 'q'
    
    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        positions = self.posvec.getPosArray(1,0,0,0,False,board)
        positions+= self.posvec.getPosArray(-1,0,0,0,False,board)
        positions+= self.posvec.getPosArray(0,1,0,0,False,board)
        positions+= self.posvec.getPosArray(0,-1,0,0,False,board)
        positions+= self.posvec.getPosArray(0,0,1,0,False,board)
        positions+= self.posvec.getPosArray(0,0,-1,0,False,board)
        positions+= self.posvec.getPosArray(0,0,0,1,False,board)
        positions+= self.posvec.getPosArray(0,0,0,-1,False,board)
        positions+= self.posvec.getPosArray(1,1,0,0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 1, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 1, 1, 0,False,board)
        positions+= self.posvec.getPosArray(0, 1, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 0, 1, 1,False,board)

        positions+= self.posvec.getPosArray(-1, 1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 1, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, -1, 1, 0,False,board)
        positions+= self.posvec.getPosArray(0, -1, 0, 1,False,board)
        positions+= self.posvec.getPosArray(0, 0, -1, 1,False,board)

        positions+= self.posvec.getPosArray(1, -1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, -1, 0,False,board)
        positions+= self.posvec.getPosArray(1, 0, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 1, -1, 0,False,board)
        positions+= self.posvec.getPosArray(0, 1, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 0, 1, -1,False,board)

        positions+= self.posvec.getPosArray(-1, -1, 0, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, -1, 0,False,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, -1, -1, 0,False,board)
        positions+= self.posvec.getPosArray(0, -1, 0, -1,False,board)
        positions+= self.posvec.getPosArray(0, 0, -1, -1,False,board)
        self.positions = positions
        return positions

class King(Piece):
    def __init__(self,spos,sColor,board):
        self.board = board
        self.score = 1e8
        self.started=False
        self.selected = False
        self.ogcolor = sColor
        self.boxes = []
        self.base = compound([cylinder(pos=spos+vector(0,0,0),radius=0.4,length=1.2,axis=vector(0,1,0),color=sColor),box(height=0.6,width=0.6,length=0.6,pos=spos+vector(0,1.5,0),color=sColor)])
        self.x = round(self.base.pos.x)
        self.y = round(ytoy(self.base.pos.y))
        self.z = round(ztoz(self.base.pos.z))
        self.d = round(ztod(self.base.pos.z))
        self.posvec = fvec.Fvector(self.x,self.y,self.z,self.d)
    
    def __repr__(self):
        return 'K'
    
    def getpositions(self,x,y,z,d,board):
        self.posvec = fvec.Fvector(x,y,z,d)
        positions = self.posvec.getPosArray(1,0,0,0,True,board)
        positions+= self.posvec.getPosArray(-1,0,0,0,True,board)
        positions+= self.posvec.getPosArray(0,1,0,0,True,board)
        positions+= self.posvec.getPosArray(0,-1,0,0,True,board)
        positions+= self.posvec.getPosArray(0,0,1,0,True,board)
        positions+= self.posvec.getPosArray(0,0,-1,0,True,board)
        positions+= self.posvec.getPosArray(0,0,0,1,True,board)
        positions+= self.posvec.getPosArray(0,0,0,-1,True,board)
        positions+= self.posvec.getPosArray(1,1,0,0,True,board)
        positions+= self.posvec.getPosArray(1, 0, 1, 0,True,board)
        positions+= self.posvec.getPosArray(1, 0, 0, 1,True,board)
        positions+= self.posvec.getPosArray(0, 1, 1, 0,True,board)
        positions+= self.posvec.getPosArray(0, 1, 0, 1,True,board)
        positions+= self.posvec.getPosArray(0, 0, 1, 1,True,board)

        positions+= self.posvec.getPosArray(-1, 1, 0, 0,True,board)
        positions+= self.posvec.getPosArray(-1, 0, 1, 0,True,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, 1,True,board)
        positions+= self.posvec.getPosArray(0, -1, 1, 0,True,board)
        positions+= self.posvec.getPosArray(0, -1, 0, 1,True,board)
        positions+= self.posvec.getPosArray(0, 0, -1, 1,True,board)

        positions+= self.posvec.getPosArray(1, -1, 0, 0,True,board)
        positions+= self.posvec.getPosArray(1, 0, -1, 0,True,board)
        positions+= self.posvec.getPosArray(1, 0, 0, -1,True,board)
        positions+= self.posvec.getPosArray(0, 1, -1, 0,True,board)
        positions+= self.posvec.getPosArray(0, 1, 0, -1,True,board)
        positions+= self.posvec.getPosArray(0, 0, 1, -1,True,board)

        positions+= self.posvec.getPosArray(-1, -1, 0, 0,True,board)
        positions+= self.posvec.getPosArray(-1, 0, -1, 0,True,board)
        positions+= self.posvec.getPosArray(-1, 0, 0, -1,True,board)
        positions+= self.posvec.getPosArray(0, -1, -1, 0,True,board)
        positions+= self.posvec.getPosArray(0, -1, 0, -1,True,board)
        positions+= self.posvec.getPosArray(0, 0, -1, -1,True,board)
        self.positions = positions
        return positions

def ztoz(z):        
    if(z>=15):
        z=z-15
    elif(z>=10):
        z=z-10
    elif(z>=5):
        z=z-5
    return z

def ztod(d):
    return int(d/5)

def ytoy(y):
    return y/2.5
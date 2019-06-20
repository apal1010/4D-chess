from vpython import *
#made using vpython, download instructions at vpython.org
import piece
from numpy import empty
import fvector as fvec
from move import Move
import node
from copy import copy
from random import shuffle
from itertools import product

scene.width = 900
scene.height = 450
class Board:

    def __init__(self):
        scene.title = 'loading'
        scene.center=vector(1.5,5,9)
        self.node_count = 0
        'Builds board and places pieces'
        self.winner = None
        self.max_depth = 3
        self.gameover = False
        self.spots = empty([4,4,4,4], dtype = piece.Piece)
        self.selectedpiece=None
        self.whitekingpos = None
        self.redkingpos = None
        self.whitepieces = []
        self.redpieces = []
        self.takenwhitepieces = []
        self.takenredpieces = []
        self.makeBoard()
        self.placePieces()
        self.currcol = color.white
        self.redscore = 111
        self.whitescore = 111
        self.redai = False
        self.whiteai = False
        
    

    def addPiece(self,x,y,z,d,piece):
        self.spots[d][z][y][x] = piece
        pos = piece.base.pos
        newpos = vector(x,y*1.5+pos.y,z+(5*d))
        piece.base.pos = newpos
        if(piece.ogcolor==color.red):
            self.redpieces.append(piece)
        else:
            self.whitepieces.append(piece)
        
    
    def selectPiece(self):
        obj = scene.mouse.pick
        if(obj!=None):
            pos = obj.pos
            if(isinstance(obj, box)):
                return False
            tx = round(pos.x)
            ty = round(self.ytoy(pos.y))
            tz = round(self.ztoz(pos.z))
            td = round(self.ztod(pos.z))
            piece = self.spots[td][tz][ty][tx]
            if(piece.ogcolor!=self.currcol):
                return False
            obj.color = color.green
            piece.select()
            kingpos = self.whitekingpos if self.currcol==color.white else self.redkingpos
            piece.glowlegal(kingpos,self.spots)
            self.selectedpiece=piece
            return True
        else:
            return False

    def moveMousePiece(self):
        obj = scene.mouse.pick
        if(obj!=None):
            fx = round(self.selectedpiece.base.pos.x)
            fy = round(self.ytoy(self.selectedpiece.base.pos.y))
            fz = round(self.ztoz(self.selectedpiece.base.pos.z))
            fd = round(self.ztod(self.selectedpiece.base.pos.z))
            fromvec = fvec.Fvector(fx,fy,fz,fd)
            pos = obj.pos
            bx = round(pos.x)
            by = round(self.ytoy(pos.y))
            bz = round(self.ztoz(pos.z))
            bd = round(self.ztod(pos.z))
            boardvec = fvec.Fvector(bx,by,bz,bd)
            piece = self.spots[fd][fz][fy][fx]
            if(fromvec==boardvec):
                self.selectedpiece = None
                piece.select()
                piece.base.color=piece.ogcolor
                piece.unglow()
                return False
            tx = round(pos.x)
            ty = round(self.ytoy(pos.y))
            tz = round(self.ztoz(pos.z))
            td = round(self.ztod(pos.z))
            tovec = fvec.Fvector(tx,ty,tz,td)
            if(tovec in piece.positions):
                self.movePiece(fx,fy,fz,fd,tx,ty,tz,td)
                return True
            else:
                self.selectedpiece = None
                piece.select()
                piece.base.color=piece.ogcolor
                piece.unglow()
                return False
        else:
            self.selectedpiece.select()
            self.selectedpiece.base.color=self.selectedpiece.ogcolor
            self.selectedpiece.unglow()
            self.selectedpiece = None
            return False

    def ztoz(self,z):
        if(z>=15):
            z=z-15
        elif(z>=10):
            z=z-10
        elif(z>=5):
            z=z-5
        return z

    def ztod(self,d):
        return int(d/5)
    
    def ytoy(self, y):
        return y/2.5

    def aimove(self):
        movec = self.ab_make_move()
        self.movePiece(movec.fromvec.x,movec.fromvec.y,movec.fromvec.z,movec.fromvec.d,movec.tovec.x,movec.tovec.y,movec.tovec.z,movec.tovec.d)

    def ab_make_move(self):
        cloc = color.red if self.currcol==color.white else color.white
        newboard = node.Node(copy(self.spots),None,self.redscore,self.whitescore,self.currcol)
        newboard.redkingpos=self.redkingpos
        newboard.whitekingpos=self.whitekingpos
        possible_moves = recpickmove(newboard,True)
        alpha = float('-inf')
        beta = float('inf')
        best_move = possible_moves[0]
        finalmoves = []
        for nud in possible_moves:
            if checkplz(nud.board,cloc):
                continue
            movem,board_value = self.ab_minimax(nud, alpha, beta, 1)
            nud.setval(board_value)
            finalmoves.append(nud)
            if alpha < board_value:
                alpha = board_value
                best_move = nud
                best_move.value = alpha
        possible_moves= [nud for nud in finalmoves if nud.value==alpha]
        shuffle(possible_moves)
        best_move = max(possible_moves,key=node.Node.getval)
        # best_move at this point stores the move with the highest heuristic
        return best_move.move

    def ab_minimax(self, mnode, alpha, beta, current_depth):
        current_depth += 1
        bnode = mnode
        if current_depth == self.max_depth:
            board_value = mnode.redscore-mnode.whitescore if self.currcol == color.red else mnode.whitescore-mnode.redscore
            if current_depth % 2 == 0:
                # pick largest number, where root is black and even depth
                if (alpha < board_value):
                    alpha = board_value
                self.node_count += 1
                return mnode, alpha
            else:
                # pick smallest number, where root is black and odd depth
                if (beta > board_value):
                    beta = board_value
                self.node_count += 1
                return mnode, beta
        if current_depth % 2 == 0:
            # min player's turn
            for child_node in mnode.getmoves():
                if alpha < beta:
                    somenode,board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if beta > board_value:
                        beta = board_value
                        bnode=child_node
            return (bnode,beta)
        else:
            # max player's turn
            for child_node in mnode.getmoves():
                if alpha < beta:
                    somenode, board_value = self.ab_minimax(child_node,alpha, beta, current_depth)
                    if alpha < board_value:
                        alpha = board_value
                        bnode=child_node
            return (bnode,alpha)
            

    def movePiece(self,fx,fy,fz,fd,tx,ty,tz,td):
        'Takes pice from square fx,fy and moves to tx,ty'
        'Checks if piece exists on square'
        piec = self.spots[fd][fz][fy][fx]
        if piece == None:
            return
        topiece = self.spots[td][tz][ty][tx]
        if topiece != None:
            if(self.currcol==color.white):
                self.redscore-=topiece.score
            else:
                self.whitescore-=topiece.score
            topiece.setvisible(0)
        y = piec.base.pos.y-(2.5*fy)
        if(piec.move(vector(tx,y+ty*2.5,tz+(5*td)))):
            self.selectedpiece = None
            piec.select()
            self.spots[fd][fz][fy][fx] = None
            self.spots[td][tz][ty][tx] = piec
            if(isinstance(piec, piece.King)):
                if(piec.ogcolor==color.red):
                    self.redkingpos = fvec.Fvector(tx,ty,tz,td)
                else:
                    self.whitekingpos = fvec.Fvector(tx,ty,tz,td)
            #if(isinstance(piec,piece.Pawn)):
                #self.promote(piec)
            piec.unglow()
        if(topiece!=None and isinstance(topiece,piece.King)):
            self.gameover = True
            self.winner = 'red' if self.currcol==color.red else 'white'

    def promote(self, piec):
        posvec = piec.getpos()
        c = 0 if piec.ogcolor==color.red else 3
        if(posvec.z == c and posvec.d == c):
            picked = False
            while(not picked):
                scene.caption = 'Please choose a piece to upgrade your pawn to q/k/r/b'
                ev = scene.waitfor('keydown')
                if ev.event == 'keydown':
                    picked = True
                    if ev.key == 'q':
                        col = self.spots[posvec.d][posvec.z][posvec.y][posvec.x].ogcolor
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x].setvisible(False)
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x] = None
                        self.addPiece(posvec.x,posvec.y,posvec.z,posvec.d,piece.Queen(vector(posvec.x,posvec.y,posvec.z),col,self.spots))
                    elif ev.key == 'k':
                        col = self.spots[posvec.d][posvec.z][posvec.y][posvec.x].ogcolor
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x].setvisible(False)
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x] = None
                        self.addPiece(posvec.x,posvec.y,posvec.z,posvec.d,piece.Knight(vector(posvec.x,posvec.y,posvec.z),col,self.spots))
                    elif ev.key == 'b':
                        col = self.spots[posvec.d][posvec.z][posvec.y][posvec.x].ogcolor
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x].setvisible(False)
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x] = None
                        self.addPiece(posvec.x,posvec.y,posvec.z,posvec.d,piece.Bishop(vector(posvec.x,posvec.y,posvec.z),col,self.spots))
                    elif ev.key == 'r':
                        col = self.spots[posvec.d][posvec.z][posvec.y][posvec.x].ogcolor
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x].setvisible(False)
                        self.spots[posvec.d][posvec.z][posvec.y][posvec.x] = None
                        self.addPiece(posvec.x,posvec.y,posvec.z,posvec.d,piece.Rook(vector(posvec.x,posvec.y,posvec.z),col,self.spots))
                    else:
                        picked = False

        else:
            return False

    def makeBoard(self):
        for d, k, i, j in product(range(4), repeat=4):
            if (i+j+k+d) % 2 == 1:
                sColor = color.blue
            else: 
                sColor = color.white
            box(pos=vector(i,(k*2.5),j+(5*d)),length=1,height=0.1,width=1,color=sColor)

    def spawnPiece(self, piecetype, team, x,y,z,d):
        col = color.white
        if(team == 1):
            col=color.red
        if(piecetype == 'pawn'):
            self.addPiece(x,y,z,d,piece.Pawn(vector(x,y,z),col,self.spots))
        if(piecetype == 'knight'):
            self.addPiece(x,y,z,d,piece.Knight(vector(x,y,z),col,self.spots))
        if(piecetype == 'rook'):
            self.addPiece(x,y,z,d,piece.Rook(vector(x,y,z),col,self.spots))
        if(piecetype == 'bishop'):
            self.addPiece(x,y,z,d,piece.Bishop(vector(x,y,z),col,self.spots))
        if(piecetype == 'king'):
            self.addPiece(x,y,z,d,piece.King(vector(x,y,z),col,self.spots))
            if(col==color.red):
                self.redkingpos = fvec.Fvector(x,y,z,d)
            else:
                self.whitekingpos = fvec.Fvector(x,y,z,d)
        if(piecetype == 'queen'):
            self.addPiece(x,y,z,d,piece.Queen(vector(x,y,z),col,self.spots))
            
    def check(self,ocol):
        kingvec = self.redkingpos if ocol==color.white else self.whitekingpos
        attacks = []
        pd=0
        for d in self.spots:
            pz=0
            for z in d:
                py=0
                for y in z:
                    px=0
                    for x in y:
                        if(x!=None):
                            if(x.ogcolor==ocol):
                                attacks+=x.getpositions(px,py,pz,pd,self.spots)
                        px+=1
                    py+=1
                pz+=1
            pd+=1
        for kack in attacks:
            if isinstance(self.spots[kack.d][kack.z][kack.y][kack.x],piece.King):
                return True
        return False



    def placePieces(self):
        Rook = 'rook'
        Knight = 'knight'
        Queen = 'queen'
        King = 'king'
        Bishop = 'bishop'
        Pawn = 'pawn'
        self.spawnPiece(Rook, 0, 0, 0, 0, 0)
        self.spawnPiece(Knight, 0, 1, 0, 0, 0)
        self.spawnPiece(Knight, 0, 2, 0, 0, 0)
        self.spawnPiece(Rook, 0, 3, 0, 0, 0)
        self.spawnPiece(Bishop, 0, 0, 1, 0, 0)
        self.spawnPiece(Queen, 0, 1, 1, 0, 0)
        self.spawnPiece(Pawn, 0, 2, 1, 0, 0)
        self.spawnPiece(Bishop, 0, 3, 1, 0, 0)
        self.spawnPiece(Bishop, 0, 0, 2, 0, 0)
        self.spawnPiece(Queen, 0, 1, 2, 0, 0)
        self.spawnPiece(King, 0, 2, 2, 0, 0)
        self.spawnPiece(Bishop, 0, 3, 2, 0, 0)
        self.spawnPiece(Rook, 0, 0, 3, 0, 0)
        self.spawnPiece(Knight, 0, 1, 3, 0, 0)
        self.spawnPiece(Knight, 0, 2, 3, 0, 0)
        self.spawnPiece(Rook, 0, 3, 3, 0, 0)
        
        self.spawnPiece(Pawn, 0, 0, 0, 1, 0)
        self.spawnPiece(Pawn, 0, 1, 0, 1, 0)
        self.spawnPiece(Pawn, 0, 2, 0, 1, 0)
        self.spawnPiece(Pawn, 0, 3, 0, 1, 0)
        self.spawnPiece(Pawn, 0, 0, 1, 1, 0)
        self.spawnPiece(Pawn, 0, 1, 1, 1, 0)
        self.spawnPiece(Pawn, 0, 2, 1, 1, 0)
        self.spawnPiece(Pawn, 0, 3, 1, 1, 0)
        self.spawnPiece(Pawn, 0, 0, 2, 1, 0)
        self.spawnPiece(Pawn, 0, 1, 2, 1, 0)
        self.spawnPiece(Pawn, 0, 2, 2, 1, 0)
        self.spawnPiece(Pawn, 0, 3, 2, 1, 0)
        self.spawnPiece(Pawn, 0, 0, 3, 1, 0)
        self.spawnPiece(Pawn, 0, 1, 3, 1, 0)
        self.spawnPiece(Pawn, 0, 2, 3, 1, 0)
        self.spawnPiece(Pawn, 0, 3, 3, 1, 0)
        
        self.spawnPiece(Pawn, 0, 0, 0, 0, 1)
        self.spawnPiece(Pawn, 0, 1, 0, 0, 1)
        self.spawnPiece(Pawn, 0, 2, 0, 0, 1)
        self.spawnPiece(Pawn, 0, 3, 0, 0, 1)
        self.spawnPiece(Pawn, 0, 0, 1, 0, 1)
        self.spawnPiece(Pawn, 0, 1, 1, 0, 1)
        self.spawnPiece(Pawn, 0, 2, 1, 0, 1)
        self.spawnPiece(Pawn, 0, 3, 1, 0, 1)
        self.spawnPiece(Pawn, 0, 0, 2, 0, 1)
        self.spawnPiece(Pawn, 0, 1, 2, 0, 1)
        self.spawnPiece(Pawn, 0, 2, 2, 0, 1)
        self.spawnPiece(Pawn, 0, 3, 2, 0, 1)
        self.spawnPiece(Pawn, 0, 0, 3, 0, 1)
        self.spawnPiece(Pawn, 0, 1, 3, 0, 1)
        self.spawnPiece(Pawn, 0, 2, 3, 0, 1)
        self.spawnPiece(Pawn, 0, 3, 3, 0, 1)
        
        self.spawnPiece(Pawn, 0, 0, 0, 1, 1)
        self.spawnPiece(Pawn, 0, 1, 0, 1, 1)
        self.spawnPiece(Pawn, 0, 2, 0, 1, 1)
        self.spawnPiece(Pawn, 0, 3, 0, 1, 1)
        self.spawnPiece(Pawn, 0, 0, 1, 1, 1)
        self.spawnPiece(Pawn, 0, 1, 1, 1, 1)
        self.spawnPiece(Pawn, 0, 2, 1, 1, 1)
        self.spawnPiece(Pawn, 0, 3, 1, 1, 1)
        self.spawnPiece(Pawn, 0, 0, 2, 1, 1)
        self.spawnPiece(Pawn, 0, 1, 2, 1, 1)
        self.spawnPiece(Pawn, 0, 2, 2, 1, 1)
        self.spawnPiece(Pawn, 0, 3, 2, 1, 1)
        self.spawnPiece(Pawn, 0, 0, 3, 1, 1)
        self.spawnPiece(Pawn, 0, 1, 3, 1, 1)
        self.spawnPiece(Pawn, 0, 2, 3, 1, 1)
        self.spawnPiece(Pawn, 0, 3, 3, 1, 1)

        l = 3
        m = l - 1
        
        self.spawnPiece(Rook, 1, 0, 0, l, l)
        self.spawnPiece(Knight, 1, 1, 0, l, l)
        self.spawnPiece(Knight, 1, 2, 0, l, l)
        self.spawnPiece(Rook, 1, 3, 0, l, l)
        self.spawnPiece(Bishop, 1, 0, 1, l, l)
        self.spawnPiece(Queen, 1, 1, 1, l, l)
        self.spawnPiece(Pawn, 1, 2, 1, l, l)
        self.spawnPiece(Bishop, 1, 3, 1, l, l)
        self.spawnPiece(Bishop, 1, 0, 2, l, l)
        self.spawnPiece(Queen, 1, 1, 2, l, l)
        self.spawnPiece(King, 1, 2, 2, l, l)
        self.spawnPiece(Bishop, 1, 3, 2, l, l)
        self.spawnPiece(Rook, 1, 0, 3, l, l)
        self.spawnPiece(Knight, 1, 1, 3, l, l)
        self.spawnPiece(Knight, 1, 2, 3, l, l)
        self.spawnPiece(Rook, 1, 3, 3, l, l)
        
        self.spawnPiece(Pawn, 1, 0, 0, m, l)
        self.spawnPiece(Pawn, 1, 1, 0, m, l)
        self.spawnPiece(Pawn, 1, 2, 0, m, l)
        self.spawnPiece(Pawn, 1, 3, 0, m, l)
        self.spawnPiece(Pawn, 1, 0, 1, m, l)
        self.spawnPiece(Pawn, 1, 1, 1, m, l)
        self.spawnPiece(Pawn, 1, 2, 1, m, l)
        self.spawnPiece(Pawn, 1, 3, 1, m, l)
        self.spawnPiece(Pawn, 1, 0, 2, m, l)
        self.spawnPiece(Pawn, 1, 1, 2, m, l)
        self.spawnPiece(Pawn, 1, 2, 2, m, l)
        self.spawnPiece(Pawn, 1, 3, 2, m, l)
        self.spawnPiece(Pawn, 1, 0, 3, m, l)
        self.spawnPiece(Pawn, 1, 1, 3, m, l)
        self.spawnPiece(Pawn, 1, 2, 3, m, l)
        self.spawnPiece(Pawn, 1, 3, 3, m, l)
        
        self.spawnPiece(Pawn, 1, 0, 0, l, m)
        self.spawnPiece(Pawn, 1, 1, 0, l, m)
        self.spawnPiece(Pawn, 1, 2, 0, l, m)
        self.spawnPiece(Pawn, 1, 3, 0, l, m)
        self.spawnPiece(Pawn, 1, 0, 1, l, m)
        self.spawnPiece(Pawn, 1, 1, 1, l, m)
        self.spawnPiece(Pawn, 1, 2, 1, l, m)
        self.spawnPiece(Pawn, 1, 3, 1, l, m)
        self.spawnPiece(Pawn, 1, 0, 2, l, m)
        self.spawnPiece(Pawn, 1, 1, 2, l, m)
        self.spawnPiece(Pawn, 1, 2, 2, l, m)
        self.spawnPiece(Pawn, 1, 3, 2, l, m)
        self.spawnPiece(Pawn, 1, 0, 3, l, m)
        self.spawnPiece(Pawn, 1, 1, 3, l, m)
        self.spawnPiece(Pawn, 1, 2, 3, l, m)
        self.spawnPiece(Pawn, 1, 3, 3, l, m)
        
        self.spawnPiece(Pawn, 1, 0, 0, m, m)
        self.spawnPiece(Pawn, 1, 1, 0, m, m)
        self.spawnPiece(Pawn, 1, 2, 0, m, m)
        self.spawnPiece(Pawn, 1, 3, 0, m, m)
        self.spawnPiece(Pawn, 1, 0, 1, m, m)
        self.spawnPiece(Pawn, 1, 1, 1, m, m)
        self.spawnPiece(Pawn, 1, 2, 1, m, m)
        self.spawnPiece(Pawn, 1, 3, 1, m, m)
        self.spawnPiece(Pawn, 1, 0, 2, m, m)
        self.spawnPiece(Pawn, 1, 1, 2, m, m)
        self.spawnPiece(Pawn, 1, 2, 2, m, m)
        self.spawnPiece(Pawn, 1, 3, 2, m, m)
        self.spawnPiece(Pawn, 1, 0, 3, m, m)
        self.spawnPiece(Pawn, 1, 1, 3, m, m)
        self.spawnPiece(Pawn, 1, 2, 3, m, m)
        self.spawnPiece(Pawn, 1, 3, 3, m, m)

    def checkmate(self):
        kingpos = self.whitekingpos if self.currcol==color.white else self.redkingpos
        pd=0
        for d in self.spots:
            pz=0
            for z in d:
                py=0
                for y in z:
                    px=0
                    for x in y:
                        if(x!=None):
                            if(x.ogcolor==self.currcol):
                                if(len(x.completepositions(px,py,pz,pd,kingpos,self.spots))!=0):
                                    return False
                        px+=1
                    py+=1
                pz+=1
            pd+=1
        return True
        

def checkplz(board,ocol):
    pd=0
    for d in board:
        pz=0
        for z in d:
            py=0
            for y in z:
                px=0
                for x in y:
                    if(x!=None):
                        if(x.ogcolor==ocol):
                            attacks=x.getpositions(px,py,pz,pd,board)
                            for kack in attacks:
                                if isinstance(board[kack.d][kack.z][kack.y][kack.x],piece.King): #and board[kack.d][kack.z][kack.y][kack.x].ogcolor!=ocol:
                                    return True
                    px+=1
                py+=1
            pz+=1
        pd+=1
    return False

def possiblemoves(board,col,kingpos):
    moves = []
    pd=0
    for d in board:
        pz=0
        for z in d:
            py=0
            for y in z:
                px=0
                for p in y:
                    if(p!=None):
                        if(p.ogcolor.equals(col)):
                            for attack in p.getpositions(px,py,pz,pd,board):
                                moves.append(Move(p.getpos(),attack))
                    px+=1
                py+=1
            pz+=1
        pd+=1
    return moves

def recpickmove(currnode,switchcol):
        boards = []
        ogboard = copy(currnode.board)
        cloc = (color.red if currnode.ccol==color.white else color.white) if switchcol else currnode.ccol
        kingpos = currnode.redkingpos if currnode.ccol==color.red else currnode.whitekingpos
        moves = possiblemoves(currnode.board,currnode.ccol,kingpos)
        redscore = currnode.redscore
        whitescore = currnode.whitescore
        i = 0
        for movec in moves:
            redscore = currnode.redscore
            whitescore = currnode.whitescore
            board = copy(ogboard)
            frovec = movec.getfromvec()
            tvec = movec.gettovec()
            piec = board[frovec.d][frovec.z][frovec.y][frovec.x]
            if piec == None:
                continue
            topiece = board[tvec.d][tvec.z][tvec.y][tvec.x]
            if topiece != None:
                if(currnode.ccol==color.white):
                    redscore-=topiece.score
                else:
                    whitescore-=topiece.score
            board[frovec.d][frovec.z][frovec.y][frovec.x] = None
            board[tvec.d][tvec.z][tvec.y][tvec.x] = piec
            piec.started = True
            newboard = node.Node(board,movec,redscore,whitescore,cloc)
            if(isinstance(piec, piece.King)):
                if(piec.ogcolor==color.red):
                    newboard.redkingpos = fvec.Fvector(tvec.x,tvec.y,tvec.z,tvec.d)
                else:
                    newboard.whitekingpos = fvec.Fvector(tvec.x,tvec.y,tvec.z,tvec.d)
            boards.append(newboard)
        return boards

def rungame():
    thisBoard = Board()
    def whiteaicheck(b):
        if b.checked:
            thisBoard.whiteai = True
        else:
            thisBoard.whiteai = False
    checkbox(bind=whiteaicheck, text='White AI') 
    def redaicheck(b):
        if b.checked:
            thisBoard.redai = True
        else:
            thisBoard.redai = False
    checkbox(bind=redaicheck, text='Red AI') 

    while True:
        if(thisBoard.checkmate()):
            thisBoard.gameover = True
            thisBoard.winner = 'white' if thisBoard.currcol==color.red else 'red'
        name = 'white' if thisBoard.currcol==color.white else 'red'
        redcheck = 'red is in check!' if thisBoard.check(color.white) else 'red is not in check'
        whitecheck = 'white is in check!' if thisBoard.check(color.red) else 'white is not in check'
        scene.title=('it is '+name+'s turn'+'\n'+redcheck+'\n'+whitecheck)
        if(thisBoard.gameover):
            scene.caption=thisBoard.winner+' wins!'
            break
        ai = thisBoard.redai if thisBoard.currcol==color.red else thisBoard.whiteai
        if(ai):
            thisBoard.aimove()
            thisBoard.currcol = color.red if thisBoard.currcol==color.white else color.white
        
        else:
            ev = scene.waitfor('click')
            selected = False
            if ev.event == 'click':
                selected = thisBoard.selectPiece()
            if(selected):
                ev2 = scene.waitfor('click')
                if ev2.event == 'click':
                    if(thisBoard.moveMousePiece()):
                        thisBoard.currcol = color.red if thisBoard.currcol==color.white else color.white


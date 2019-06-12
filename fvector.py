from vpython import*
import piece
import copy
def legal(x):
    if(x<0):
        return False
    elif(x>3):
        return False
    return True

def legalpos(x,y,z,d):
    return(legal(x) and legal(y) and legal(z) and legal(d))

class Fvector:
    def __init__(self,x,y,z,d):
        self.x = x
        self.y = y
        self.z = z
        self.d = d

    def __str__(self):
        return "<"+str(self.x)+","+str(self.y)+","+str(self.z)+","+str(self.d)+">"

    def __eq__(self, obj):
        if(obj!=None):
            return obj.x == self.x and obj.y == self.y and obj.z == self.z and obj.d == self.d
    
    def getPosArray(self,x,y,z,d,limited,board):
        arr = []
        i=x+self.x
        j=y+self.y
        k=z+self.z
        l=d+self.d
        
        while(legalpos(i,j,k,l)):
            f = Fvector(i,j,k,l)
            if(board[l][k][j][i]!=None):
                if(board[l][k][j][i].ogcolor.equals(board[self.d][self.z][self.y][self.x].ogcolor)):
                    break
                else:
                    arr.append(f)
                    break
            else:
                arr.append(f)
            i+=x
            j+=y
            k+=z
            l+=d
            if(limited):
                break
        return arr

    def pawn(self,x,y,z,d,limited,board):
        arr = []
        i=x+self.x
        j=y+self.y
        k=z+self.z
        l=d+self.d
        while(legalpos(i,j,k,l)):
            f = Fvector(i,j,k,l)
            if(x==0 and y==0 and d==0):
                if(board[l][k][j][i]!=None):
                    break
                else:
                    arr.append(f)
            elif(board[l][k][j][i]!=None):
                if(board[self.d][self.z][self.y][self.x]==None):
                    print(self)
                if(not board[l][k][j][i].ogcolor.equals(board[self.d][self.z][self.y][self.x].ogcolor)):
                    arr.append(f)

            i+=x
            j+=y
            k+=z
            l+=d
            if(limited):
                break
            limited = True
        return arr

    def removecheckpos(self,mpiece,board,kingpos):
        

        newarr =[]
        for move in mpiece.getpositions(self.x,self.y,self.z,self.d,board):
            nboard = copy.copy(board)
            piec = nboard[self.d][self.z][self.y][self.x]
            if piec == None:
                continue
            topiece = nboard[move.d][move.z][move.y][move.x]
            nboard[self.d][self.z][self.y][self.x] = None
            nboard[move.d][move.z][move.y][move.x] = piec
            from chessboard import checkplz
            cloc = color.red if mpiece.ogcolor==color.white else color.white
            if not checkplz(nboard,cloc):
                newarr.append(move)
            nboard[self.d][self.z][self.y][self.x] = piec
            nboard[move.d][move.z][move.y][move.x] = topiece
        
        return newarr


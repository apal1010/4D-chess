class Node:
    def __init__(self,board,movve,rscore,wscore,ccol):
        self.board = board
        self.move = movve
        self.redscore = rscore
        self.whitescore = wscore
        self.ccol = ccol
        self.value = 0
        self.redkingpos = None
        self.whitekingpos = None

    def setval(self, val):
        self.value = val

    def getval(self):
        return self.value

    def getmoves(self):
        from chessboard import recpickmove
        boards= recpickmove(self,False)
        #print(len(boards))
        return boards


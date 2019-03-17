from fvector import Fvector
class Move:
    def __init__(self, fromvecc, tovecc):
        self.fromvec = fromvecc
        self.tovec = tovecc
        self.value = 0

    def getfromvec(self):
        return self.fromvec

    def gettovec(self):
        return self.tovec

    def __repr__(self):
        return str(self.fromvec)+str(self.tovec)
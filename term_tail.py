from node import Node
from utils import calcByTerm

class TermTail(Node):
    def __init__(self, op, f,  tt):
        super(__class__,self)
        self.op = op
        self.f = f
        self.tt = tt
    
    def eval(self, left):
        eval_factor = self.f.eval()
        #left = self.calc(left, eval_factor)
        left = calcByTerm(self.op, left,eval_factor)
        return self.tt.eval(left)
    
    def canonicalize(self, seq):
        pass



    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.tt)})'
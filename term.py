from node import Node
from empty import Empty
from factor_new import Constant

class Term(Node):
    def __init__(self, f, tt):
        super(__class__,self)
        self.f = f
        self.tt = tt
    
    def eval(self):
        return self.tt.eval(self.f.eval())
    
    def canonicalize(self, seq):
        term = list(seq[0])
        constant = seq[1]

        return self.tt.canonicalize(self.f.canonicalize())

    def __str__(self):
        return f'{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.tt)})'
        
class TermTail(Node):
    def __init__(self, op, f,  tt):
        super(__class__,self)
        self.op = op
        self.f = f
        self.tt = tt
    
    def eval(self, left):
        eval_factor = self.f.eval()
        #left = self.calc(left, eval_factor)
        left = self.calcByTerm(left,eval_factor, self.checkTerm)
        return self.tt.eval(left)
    
    def canonicalize(self, seq):
        pass

    def checkTerm(self, left,right):
        if isinstance(left,right.__class__):
            if isinstance(left, Constant):
                return True
            else:
                if left.expo == right.expo:
                    return True
                else:
                    return False
        else:
            return False

    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.tt)})'
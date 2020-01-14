from node import Node
from empty import Empty


class Term(Node):
    def __init__(self, f, tt):
        super(__class__,self)
        self.f = f
        self.tt = tt
    
    def eval(self):
        return self.tt.eval(self.f.eval())
    
    def canonicalize(self):
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
        left = self.calc(left, eval_factor)
        return self.tt.eval(left)
    
    def canonicalize(self, left):
        pass

    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.tt)})'
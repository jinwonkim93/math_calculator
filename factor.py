from node import Node
from empty import Empty
from expression import Expr

class Factor(Node):
    def __init__(self, e, sign = Empty(), expo = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign
        self.expo = expo

    def eval(self):
        if self.sign is '-':
            return -self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else -self.expo.eval(float(self.e))
        else:
            return self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else self.expo.eval(float(self.e))
    
    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'

class Variable(Node):
    def __init__(self, e):
        super(__class__,self)
        self.e = e
    
    def eval(self):
        #return self.e.eval() if isinstance(self.e, (Expr, Log, AngleFunction, Symbol)) else float(self.e)
        return float(self.e) if isinstance(self.e, str) else self.e.eval()
    
    def __str__(self):
        return str(self.e)
    def __repr__(self):
        return f'Variable({repr(self.e)})'
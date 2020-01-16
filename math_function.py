
from node import Node
from expression import Expr
from empty import Empty
from utils import lognNew, triangleFunction
from factor_new import Constant

class AngleFunction(Node):
    def __init__(self, symbol, e):
        super(__class__,self)
        self.symbol = symbol
        self.e = e
    def eval(self):
        self.e = self.e.eval()
        return triangleFunction(self, self.e)
    
    def __str__(self):
        return f'{str(self.symbol)}({str(self.e)})'
    def __repr__(self):
        return f'AngleFunction({repr(self.symbol)},{repr(self.e)})'

class Log(Node):
    def __init__(self, symbol, e):
        super(__class__,self)
        self.symbol = symbol
        self.e = e
    
    def eval(self):
        return lognNew(self.e.eval(),self.symbol)
        
    def __str__(self):
        return f'log{str(self.symbol):.4}({str(self.e)})'
    def __repr__(self):
        return f'Log({repr(self.symbol)},{repr(self.e)})'

class Sin(object):
    def __init__(self,e):
        self.e = e
    
    def eval(self):
        pass

    def __str__(self):
        pass
    
    def __repr__(self):
        pass

class Cos(object):
    def __init__(self, e):
        self.e = e
    
    def eval(self):
        pass

    def __str__(self):
        pass
    
    def __repr__(self):
        pass

class Tan(object):
    def __init__(self, e):
        self.e = e
    
    def eval(self):
        pass

    def __str__(self):
        pass
    
    def __repr__(self):
        pass
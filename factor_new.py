#from node import Node
from empty import Empty
from expression import Expr

class Factor(object):
    def __init__(self, e, sign = Empty(), expo = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign
        self.expo = expo

    """    
    def eval(self):
        if self.sign is '-':
            return -self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else -self.expo.eval(float(self.e))
        else:
            return self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else self.expo.eval(float(self.e))
    """
    def eval(self):
        return -self.expo.eval(self.e.eval()) if self.sign is '-' else self.expo.eval(self.e.eval())
    
    def canonicalize(self):
        canonicalized_e = self.expo.canonicalize(self.e.canonicalize())
        if isinstance(canonicalized_e, Variable):
            return -self.expo.canonicalize(self.e.canonicalize()) if self.sign is '-' else self.expo.canonicalize(self.e.canonicalize())

    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'

class Variable(object):
    def __init__(self, e, coeff = 1, expo = 1):
        self.coeff = coeff
        self.e = e
        self.expo = expo
    
    
    def __add__(self, other):
        if type(self) == type(other):
            if self.e.symbol == other.e.symbol and self.expo == other.expo:
                coeff = self.coeff + other.coeff
                return Variable(self.e, coeff = coeff) if coeff is not 0 else Constant(0)
        return [self,"+", other]
    
    def __sub__(self,other):
        if type(self) == type(other):
            if self.e.symbol == other.e.symbol and self.expo == other.expo:
                coeff = self.coeff - other.coeff
                return Variable(self.e, coeff = coeff) if coeff is not 0 else Constant(0)
        return [self, '-', other]
    
    def __mul__(self, other):
        if type(self) == type(other):
            if self.e.symbol == other.e.symbol:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else Constant(0)
            else:
                return [self, "*", other]
        coeff = self.coeff * other.value
        return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
              
    def __truediv__(self, other):
        if type(self) == type(other):
            if self.e.symbol == other.e.symbol:
                coeff = self.coeff / other.coeff
                expo = self.expo - other.expo
                return Variable(self.e, coeff = coeff, expo = expo)
            else:
                return [self, "/", other]
        coeff = self.coeff / other.value
        return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)

    def __neg__(self):
        return Variable(self.e,coeff= -self.coeff, expo = self.expo) if coeff is not 0 else Constant(0)

    def __repr__(self):
        if self.coeff == 0:
            return '0'
        
        elif self.expo == 0:
            return f'{self.coeff}'
        
        elif self.coeff != 1:
            return f'{self.coeff}*{self.e.symbol}' if self.expo == 1 else f'{self.coeff}{self.e.symbol}^{self.expo}'
        else:
            return f'{self.e.symbol}' if self.expo == 1 else f'{self.e.symbol}^{self.expo}'

    def insert(self, value):
        self.value = value
    
    def calcSymbol(self):
        if self.value is not None:
            res = self.value**self.expo
            res = self.coeff * res
            return res
    
    def eval(self):
        return self if self.coeff != 0 else Constant(0)

class Symbol(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.value = None

        
    def insert(self, value):
        self.value = value
    
    def eval(self):
        return self.value.eval() if isinstance(self.value, Expr) else float(self.value)
    
    def __repr__(self):
        return f'{self.symbol}'

class Constant(object):
    def __init__(self,value):
        self.value = float(value)

    def eval(self):
        return self
    
    def canonicalize(self):
        return self
    
    def __add__(self, other):
        if isinstance(other, Variable):
            return [self, '+', other]
        else:
            return Constant(self.value + other.value)
    
    def __sub__(self, other):
        if isinstance(other, Variable):
            return [self, '-', other]
        else:
            return Constant(self.value - other.value)
    
    def __mul__(self,other):
        if isinstance(other, Variable):
            coeff = self.value * other.coeff
            return Variable(other.e, coeff = coeff, expo = other.expo )
        else:
            return Constant(self.value * other.value)
    
    def __truediv__(self,other):
        if isinstance(other, Variable):
            coeff = self.value / other.coeff
            return Variable(other.e, coeff = coeff, expo = other.expo )
        else:
            return Constant(self.value / other.value)

    def __neg__(self):
        return Constant(-self.value)

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
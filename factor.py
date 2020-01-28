from node import Node
from empty import Empty
from expression import Expr

class Factor(Node):
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
        print('factor = ', self.expo.eval(self.e.eval()))
        return -self.expo.eval(self.e.eval()) if self.sign is '-' else self.expo.eval(self.e.eval())

    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'

class Variable(Node):
    def __init__(self, e):
        super(__class__,self)
        self.coeff = 1
        self.e = e
        self.expo = 1
    
    def eval(self):
        return float(self.e) if isinstance(self.e, str) else self.e.eval()

    def canonicalize(self):
        return self

    def __str__(self):
        return str(self.e)
    def __repr__(self):
        return f'Variable({repr(self.e)})'

class Symbol(object):
    def __init__(self, symbol, coeff = 1, expo = 1):
        self.coeff = coeff
        self.symbol = symbol
        self.value = None
        self.expo = expo
    
    def __add__(self, other):
        if isinstance(other, Symbol):
            if self.symbol == other.symbol and self.expo == other.expo:
                coeff = self.coeff + other.coeff
                return Symbol(self.symbol, coeff = coeff)
        else:
            return [self,"+",other]
    
    def __sub__(self,other):
        if isinstance(other, Symbol):
            if self.symbol == other.symbol and self.expo == other.expo:
                coeff = self.coeff - other.coeff
                return Symbol(self.symbol, coeff = coeff)
        
        else:
            return [self,"-",other]
    
    def __mul__(self, other):
        if isinstance(other, Symbol):
            if self.symbol == other.symbol:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                return Symbol(self.symbol, coeff = coeff, expo = expo)
        else:
            if isinstance(other, (float,int)):
                coeff = self.coeff * other
                return Symbol(self.symbol, coeff = coeff, expo = self.expo)
            else:
                temp = []
                for element in other:
                    if isinstance(element, str): temp.append(element)
                    else:
                        temp.append(self.__mul__(element))
                return temp
                        
    
    def __truediv__(self, other):
        if isinstance(other, Symbol):
            if self.symbol == other.symbol:
                coeff = self.coeff / other.coeff
                expo = self.expo - other.expo
                return Symbol(self.symbol, coeff = coeff, expo = expo)
        else:
            if isinstance(other, (float,int)):
                coeff = self.coeff / other
                return Symbol(self.symbol, coeff = coeff, expo = self.expo)
            else:
                return [self,'/',other]
    
    def __repr__(self):
        if self.coeff == 0:
            return '0'
        
        elif self.expo == 0:
            return f'{self.coeff}'
        
        elif self.coeff != 1:
            return f'{self.coeff}{self.symbol}' if self.expo == 1 else f'{self.coeff}{self.symbol}^{self.expo}'
        else:
            return f'{self.symbol}' if self.expo == 1 else f'{self.symbol}^{self.expo}'

    def insert(self, value):
        self.value = value
    
    def calcSymbol(self):
        if self.value is not None:
            res = self.value**self.expo
            res = self.coeff * res
            return res
    def eval(self):
        return self.value.eval() if isinstance(self.value, Expr) else float(self.value)
'''
class Symbol(object):
    def __init__(self, symbol,subExpr = None):
        self.symbol = symbol
        self.value = None
        self.subExpr = subExpr
        
    def insert(self, value, subExpr = None):
        self.value = value
        self.subExpr = subExpr
    
    def eval(self):
        return self.value.eval() if isinstance(self.value, Expr) else float(self.value)
    
    def __repr__(self):
        return f'({repr(self.symbol)}' if self.subExpr is not None else f'({repr(self.symbol)})'
    def __str__(self):
        return f'({self.subExpr})' if self.subExpr is not None else f'({self.value})'
'''
class Constant(Node):
    def __init__(self,e):
        super(__class__,self)
        self.e = float(e)

    def eval(self):
        return self.e
    
    def canonicalize(self):
        return self
    
    def __str__(self):
        return str(self.e)
    
    def __repr__(self):
        return f'Constant({repr(self.e)})'
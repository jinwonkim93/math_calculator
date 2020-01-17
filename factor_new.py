#from node import Node
from empty import Empty
from expression import Expr
import math
from fractions import Fraction

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
        #factor = self.expo.eval(self.e.eval())
        return -self.expo.eval(self.e.eval()) if self.sign is '-' else self.expo.eval(self.e.eval())

    
    def canonicalize(self):
        canonicalized_e = self.expo.canonicalize(self.e.canonicalize())
        if isinstance(canonicalized_e, Variable):
            return -self.expo.canonicalize(self.e.canonicalize()) if self.sign is '-' else self.expo.canonicalize(self.e.canonicalize())

    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'


from copy import deepcopy
class Variable(object):
    def __init__(self, e, coeff = 1, expo = 1):
        self.coeff = coeff
        self.e = e
        self.expo = expo
    
    
    def __add__(self, other):
        if isinstance(other, Variable):
            if type(self.e) == type(other.e):
                if self.e.symbol == other.e.symbol and self.expo == other.expo:
                    coeff = self.coeff + other.coeff
                    return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
        return [self,"+", other]
    
    def __radd__(self, other):
        if isinstance(other, Variable):
            if type(self.e) == type(other.e):
                if self.e.symbol == other.e.symbol and self.expo == other.expo:
                    coeff = other.coeff + self.coeff
                    return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
        return [other, "+", self]
    
    def __sub__(self,other):
        print('step 3 = ', self, other)
        if isinstance(other, Variable):
            if type(self.e) == type(other.e):
                
                if self.e.symbol == other.e.symbol and self.expo == other.expo:
                    coeff = self.coeff - other.coeff
                    return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
        return [self, '-', other]

    def __rsub__(self,other):
        if isinstance(other, Variable):
            if type(self.e) == type(other):
                if self.e.symbol == other.e.symbol and self.expo == other.expo:
                    coeff = other.coeff - self.coeff
                    return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
        return [other, '-', self]
    
    def __mul__(self, other):
        if isinstance(other, Variable):
            if type(self.e) == type(other):
                if self.e.symbol == other.e.symbol:
                    coeff = self.coeff * other.coeff
                    expo = self.expo + other.expo
                    return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else Constant(0)
                else:
                    return [self, "*", other]
        coeff = self.coeff * other
        return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
    
    def __rmul__(self, other):
        if isinstance(other, Variable):
            if type(self.e) == type(other):
                if self.e.symbol == other.e.symbol:
                    coeff = self.coeff * other.coeff
                    expo = self.expo + other.expo
                    return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else Constant(0)
                else:
                    return [self, "*", other]
        elif isinstance(other, Constant):
            coeff = other.eval() * self.coeff
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
        else:
            coeff = other * self.coeff
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
              
    def __truediv__(self, other):
        print(type(other))
        if isinstance(other, Variable):
            if type(self) == type(other):
                if self.e.symbol == other.e.symbol:
                    coeff = self.coeff / other.coeff
                    expo = self.expo - other.expo
                    return Variable(self.e, coeff = coeff, expo = expo)
                else:
                    return [self, "/", other]
        coeff = self.coeff / other.eval()
        return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else Constant(0)
    
    def __rtruediv__(self, other):
        value =  None
        if isinstance(other, Variable):
            if type(self.e) == type(other):
                if self.e.symbol == other.e.symbol:
                    coeff = other.coeff / self.coeff
                    expo = other.expo - self.expo
                    return Variable(self.e, coeff = coeff, expo = expo)
                else:
                    return [other, "/", self]

        elif isinstance(other, Constant):
            value = other.eval()
        else:
            value = other
        coeff = value/self.coeff
        if coeff > 1:
            return [coeff, '/', Variable(self.e, expo = self.expo)]
        else:
            return Variable(self.e, coeff = coeff, expo = self.expo)

    def __neg__(self):
        return Variable(self.e,coeff= -self.coeff, expo = self.expo) if coeff is not 0 else Constant(0)

    def __pow__(self, other):
        res = deepcopy(self)
        res.expo = other
        return res 
        
    def __repr__(self):
        if self.coeff == 0:
            return '0'
        
        elif isinstance(self.e, Empty):
            return f'{self.coeff}' if self.expo == 1 else f'{self.coeff}^{self.expo}'
        
        elif isinstance(self.expo, (list, Variable)):
            return f'{self.coeff}*{self.e}^{self.expo}' if self.coeff != 1 else f'{self.e}^{self.expo}'
        
        elif self.coeff != 1:
            if self.expo == 0:
                return f'{self.coeff}'
            
            elif self.expo < 0:
                return f'{self.coeff}/{self.e}^{~self.expo}'
            elif self. expo == 1:
                return f'{self.coeff}*{self.e}'
            else:
                return f'{self.coeff}{self.e}^{self.expo}'
        else:
            if self.expo == 0:
                return f'{self.coeff}'
            
            elif self.expo < 0:
                return f'{self.coeff}/{self.e}^{~self.expo}'
            elif self. expo == 1:
                return f'{self.e}'
            else:
                return f'{self.e}^{self.expo}'

    def insert(self, value):
        self.value = value
    
    def calcSymbol(self):
        if isinstance(self.e, Empty):
            res = self.coeff**self.expo
            res = self.coeff * res
            return res
    
    def eval(self):
        if isinstance(self.e, float):
            return self.e
        else:
            self.e = self.e.eval()
        #if isinstance(self.e, Empty): return Constant(self.coeff * (self.e ** self.expo))
            return self if self.coeff != 0 else Constant(0)

class Symbol(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.value = None

        
    def insert(self, value):
        self.value = value
    
    def eval(self):
        #return self.value.eval() if isinstance(self.value, Expr) else float(self.value)
        return self
    
    def __repr__(self):
        return f'{self.symbol}'

"""
class Constant(object):
    def __init__(self,value, expo = Empty()):
        self.value = float(value)
        self.expo = expo
    
    def eval(self):
        return self
    
    def __add__(self, other):
        if isinstance(other, Variable):
            return [self, '+', other]
        elif isinstance(other, Constant):
            return Constant(self.value + other.value)
        else:
            return Constant(self.value + other)
    
    def __radd__(self, other):
        if isinstance(other, Variable):
            return [other, '+', self]
        elif isinstance(other, Constant):
            return Constant(self.value + other.value)
        else:
            return Constant(self.value + other)
    
    def __sub__(self, other):
        if isinstance(other, Variable):
            return [self, '-', other]
        elif isinstance(other, Constant):
            return Constant(self.value - other.value)
        else:
            return Constant(self.value - other)
    
    def __rsub__(self, other):
        if isinstance(other, Variable):
            return [other, '-', self]
        elif isinstance(other, Constant):
            return Constant(other.value - self.value)
        else:
            return Constant(other -  self.value)
    
    def __mul__(self,other):
        if isinstance(other, Variable):
            coeff = self.value * other.coeff
            return Variable(other.e, coeff = coeff, expo = other.expo )
        elif isinstance(other, Constant):
            return Constant(self.value * other.value)
        else:
            return Constant(self.value * other)
    
    def __rmul__(self,other):
        if isinstance(other, Variable):
            coeff = self.value * other.coeff
            return Variable(other.e, coeff = coeff, expo = other.expo )
        elif isinstance(other, Constant):
            return Constant(self.value * other.value)    
        else:
            return Constant(self.value * other)

    def __truediv__(self,other):
        if isinstance(other, Constant):
        #if isinstance(other, Variable):
            #coeff = self.value / other.coeff
            #return Variable(other.e, coeff = coeff, expo = other.expo )
        #else:
            return Constant(self.value / other.value)
    
    def __rtruediv__(self,other):
        value = None
        if isinstance(other, Variable):
            gcd = math.gcd(self.value, other.coeff)
            
            return [Variable(other.e, coeff = coeff/gcd, expo = other.expo ), '/', Constant(self.value/gcd)]
        elif isinstance(other, Constant):
            return Constant(other.value / self.value)
        else:
            return Constant(other / self.value)

    def __eq__(self,other):
        if isinstance(other, Constant):
            return True if self.value == other.value else False
        elif isinstance(other, float):
            return True if self.value == other else False
        else:
            return False

    def __pow__(self, other):
        if isinstance(other, Constant):
            r_raised = abs(self.value) ** other.value
            return self.__class__(r_raised)

    def __neg__(self):
        return Constant(-self.value)

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f'{self.value}' if isinstance(self.expo, Empty) else f'{self.value}^{self.expo}'
"""
class Constant(object):
    def __init__(self,value, expo = Empty()):
        self.value = float(value)
        self.expo = expo
    
    def eval(self):
        return self.value

    def __eq__(self,other):
        if isinstance(other, Constant):
            return True if self.value == other.value else False
        elif isinstance(other, float):
            return True if self.value == other else False
        else:
            return False

    def __neg__(self):
        return -self.value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f'{self.value}' if isinstance(self.expo, Empty) else f'{self.value}^{self.expo}'
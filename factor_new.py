#from node import Node
from empty import Empty
from expression import Expr
import math
from mathematical_constant import PI, E
# import math_function

def list2str(expr):
    try:
        d = ''
        for element in expr:
            if isinstance(element, list):
                element = list2str(element)
            d += str(element)
        return d
    except:
        return str(expr)

class Factor(object):
    def __init__(self, e, sign = Empty(), expo = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign
        self.expo = expo

    def eval(self):
        return -self.expo.eval(self.e.eval()) if self.sign is '-' else self.expo.eval(self.e.eval())


    def getCalc(self):
        return -self.expo.getCalc(self.e.getCalc()) if self.sign is '-' else self.expo.getCalc(self.e.getCalc())

    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
        #return f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'


from copy import deepcopy
class Variable(object):
    def __init__(self, e, coeff = 1.0, expo = 1.0):
        self.coeff = coeff
        self.e = e
        self.expo = expo
    
    def checkVariable(self, myExpr, other):
        if myExpr.e == other.e and myExpr.expo == other.expo:
            if isinstance(myExpr.coeff, (int,float)) and isinstance(other.coeff, (int,float)):
                return True
            elif isinstance(myExpr.coeff, Variable) and isinstance(other.coeff, Variable):
                 return self.checkVariable(myExpr.coeff, other.coeff)
            else:
                return False
        return False

            
    def __add__(self, other):
        if isinstance(other, Variable):
            print(self, '+', other)
            print(self.e == other.e)
            if self.checkVariable(self,other):
                coeff = self.coeff + other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            
            if isinstance(self.expo, Variable):
                return [other, "+", self]
            if other.expo > self.expo:
                return [other, "+", self]
            elif other.e < self.e:
                return [other, '+', self]
            
        return [self,"+", other]
    
    def __radd__(self, other):
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff + self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [other, "+", self]
        return [other, "+", self]
    
    def __sub__(self,other):
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = self.coeff - other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [-other, "+", self]
        return [self, '-', other]

    def __rsub__(self,other):
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff - self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [other, "-", self]
            else:
                return [-self, '+', other]
        return [other, '-', self]
    
    def __mul__(self, other):
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else 0
            elif self.e.__class__ == other.e.__class__:
                if self.e > other.e:
                    coeff = self.coeff * other
                    return Variable(self.e, coeff = coeff, expo = self.expo)
                else:
                    coeff = other.coeff * self
                    return Variable(other.e, coeff = coeff, expo = other.expo)
            else:
                coeff = other.coeff * self
                return Variable(other.e, coeff = coeff, expo = other.expo)

        else:
            coeff = self.coeff * other
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
    
    def __rmul__(self, other):
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else 0
            else:
                return [self, "*", other]
        elif isinstance(other, Constant):
            coeff = other.eval() * self.coeff
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
        else:
            coeff = other * self.coeff
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
              
    def __truediv__(self, other):
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff / other.coeff
                expo = self.expo - other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if expo != 0 else coeff
            else:
                #return self*Variable(other.e, coeff = other.coeff, expo = -other.expo)
                return [self, "/", other]
        elif isinstance(other, Constant):
            coeff = self.coeff / other.eval()
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
        else:
            coeff = self.coeff / other
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
    
    def __rtruediv__(self, other):
        value =  None
        if isinstance(other, Variable):
            if isinstance(self.e, Empty) and isinstance(other.e, Empty): return [other, "/", self]
            if self.e == other.e:
                coeff = other.coeff / self.coeff
                expo = other.expo - self.expo
                return Variable(self.e, coeff = coeff, expo = expo)
            else:
                return other*Variable(self.e, coeff = self.coeff, expo = -self.expo)

        elif isinstance(other, Constant):
            value = other.eval()
            coeff = value/self.coeff
            return Variable(self.e, coeff = coeff, expo = -self.expo).eval()
        elif isinstance(other, (int,float)):
            value = other
            if isinstance(self.e, Empty):
                coeff =  [other, "/", self]
            else:
                coeff = value/self.coeff
            return Variable(self.e, coeff = coeff, expo = -self.expo)
        else:
            raise NotImplemented

    def __neg__(self):
        return Variable(self.e,coeff= -self.coeff, expo = self.expo) if self.coeff is not 0 else 0

    def __pow__(self, other):
        res = deepcopy(self)
        res.expo = other
        return res 
    
    def __repr__(self):
        if self.coeff == 0:
            return '0'
        
        elif isinstance(self.e, Empty):
            if isinstance(self.coeff, list):
                d = list2str(self.coeff)
                return f'({d})^{self.expo}'
            return f'{self.coeff}' if self.expo == 1 else f'{self.coeff}^{self.expo}'
        
        elif isinstance(self.expo, list):
            return f'{self.coeff}*{self.e}^({self.expo})' if self.coeff != 1 else f'{self.e}^({self.expo})'
        
        elif isinstance(self.expo, Variable):
            return f'{self.coeff}*{self.e}^{self.expo}' if self.coeff != 1 else f'{self.e}^{self.expo}'
        
        elif self.coeff != 1:
            if self.expo == 0:
                return f'{self.coeff}'
            
            elif self.expo < 0:
                return f'{self.coeff}*{self.e}^{self.expo}'
            elif self. expo == 1:
                return f'{self.coeff}*{self.e}'
            else:
                return f'{self.coeff}*{self.e}^{self.expo}'
        else:
            if self.expo == 0:
                return f'{self.coeff}'
            
            elif self.expo < 0:
                return f'{self.coeff}*{self.e}^{self.expo}'
            elif self. expo == 1:
                return f'{self.e}'
            else:
                return f'{self.e}^{self.expo}'
    
    def getCalc(self):
        if isinstance(self.e, Empty):
            res = self.coeff**self.expo
            res = self.coeff * res
            return res
        if isinstance(self.e, (int,float)):
            res = self.e ** self.expo
            res = self.coeff * res
            return res
        else:
            res = self.e.getCalc()**self.expo
            res = self.coeff * res
            return res
    
    def eval(self):
        res = None
        if isinstance(self.e, float):
            return self.e
        else:
            if not isinstance(self.e, (int,float,Symbol,Empty)):
                self.e = self.e.eval()
                if isinstance(self.expo, Variable):
                    return self
                elif self.expo < 0:
                    self.e = self.e.convert()
                    self.expo = -self.expo
            return self if self.coeff != 0 else 0


    def getDerivative(self, symbol):
        if isinstance(self.e, (int,float)): return 0
        
        elif isinstance(self.expo, Variable):
            return self * Variable(Log(E,self.e).eval()).eval() * self.expo.getDerivative(symbol)
                
        elif isinstance(self.e, Empty):
            if self.coeff == E:
                expo = self.expo.getDerivative(symbol)
                return Variable(Empty(),coeff = self.coeff, expo = expo)
            else:
                return 0
        
        elif isinstance(self.e, Symbol):
            if self.e == symbol:
                if self.expo != 1:
                    coeff = self.coeff * self.expo
                    return Variable(self.e,coeff = coeff, expo = self.expo-1)
                elif self.expo == 1:
                    return self.coeff*self.expo
                
            elif isinstance(self.coeff, Variable):
        
                coeff = self.coeff.getDerivative(symbol)
                if coeff != 0:
                    coeff = coeff * Variable(self.e,expo = self.expo)
                    return coeff
            else:
                return 0
        else:
            return self.e.getDerivative(self,symbol)



class Symbol(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.value = None

        
    def insert(self, value):
        self.value = float(value)
    
    def eval(self):
        return self
    
    def getCalc(self):
        return self.value
    def __lt__(self, other):
        return self.symbol < other.symbol
    def __gt__(self, other):
        return self.symbol > other.symbol
    def __eq__(self, other):
        if other.__class__ != self.__class__: return False
        elif self.symbol == other.symbol: return True
        else: return False

    def __repr__(self):
        return f'{self.symbol}'

class Constant(object):
    def __init__(self,value, expo = Empty()):
        self.value = float(value)
        self.expo = expo
    
    def eval(self):
        return self.value
    
    def getCalc(self):
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
        if self.value == PI:
            return 'pi'
        elif self.value == E:
            return 'e'
        return str(self.value)
    
    def __repr__(self):
        return f'{self.value}' if isinstance(self.expo, Empty) else f'{self.value}^{self.expo}'

# from expression import Expr
# from empty import Empty
# from utils import isExpr
#from factor_new import Variable, Constant
from math import sin, cos, tan
# from mathematical_constant import PI, E
import numpy as np

class Log(object):
    def __init__(self, symbol, e, name = 'log'):
        super(__class__,self)
        self.symbol = float(symbol)
        self.e = e
        self.name = name
    
    def eval(self):
        try:
            # return self.lognNew(self.e.eval(),self.symbol)
            e_val = self.e.eval()
            print(e_val, type(e_val))
            return self.lognNew(e_val,self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return self.lognNew(self.e.getCalc(),self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
    
    def lognNew(self, n, x = E):
        return math.log(n) / math.log(x)
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            e_val = self.e.eval()
            coeff = variable.coeff * self.e.getDerivative(symbol)
            if isinstance(e_val, Variable):
                coeff = coeff/e_val
                return coeff
            else:
                return [coeff, '/', e_val]
        elif variable.expo > 1:
            e_val = self.e.eval()
            if isinstance(e_val, Variable):
                coeff = Variable(self, coeff = variable.coeff*variable.expo, expo = variable.expo-1)/e_val
                return coeff 

    def convert(self):
        """ e_val = self.e.eval()
        if isinstance(e_val, Variable):
            self.e = "집가서하자"
            coeff = e_eval.expo

            return Variable(,)"""
        return self
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __str__(self):
        e_eval = self.e.eval()
        print(e_eval)
        if isinstance(e_eval, list):
            e_eval = list2str(e_eval)    
            print(e_eval)
        return f'log{str(self.symbol):.4}({e_eval})'
    def __repr__(self):
        e_eval = self.e.eval()
        print(e_eval)
        if isinstance(e_eval, list):
            e_eval = list2str(e_eval)   
            print(e_eval)
        return f'Log({repr(self.symbol)},{e_eval})'

class Sin(object):
    def __init__(self,e, name = 'sin'):
        self.e = e
        self.name = name
    
    def eval(self):
        try:
            return sin(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return sin(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            return Variable(Cos(self.e), coeff = coeff)
        elif variable.expo > 1:
            try:
                coeff1 = self.e.getDerivative(symbol)
                coeff = variable.expo * coeff1 * variable.coeff
                expo = variable.expo - 1
                new_e = variable.e
                return Variable(Cos(self.e), coeff = Variable(new_e, coeff = coeff, expo = expo))
            except Exception as e:
                print(e)
    
    def convert(self):
        return Csc(self.e)
    
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'sin({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class Cos(object):
    def __init__(self, e, name = 'cos'):
        self.e = e
        self.name = name

    def eval(self):
        try:
            return cos(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return cos(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            return Variable(Sin(self.e), coeff = -coeff)
        elif variable.expo > 1:
            coeff = variable.coeff * variable.expo * self.e.getDerivative(symbol)
            expo = variable.expo - 1
            new_e = variable.e
            return Variable(Sin(self.e), coeff = Variable(new_e, coeff = -coeff, expo = expo))
    
    def convert(self):
        return Sec(self.e)

    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'cos({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class Tan(object):
    def __init__(self, e, name = 'tan'):
        self.e = e
        self.name = name
    
    def eval(self):
        try:
            return tan(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return tan(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            return Variable(Sec(self.e), coeff = coeff, expo = 2)
        elif variable.expo > 1:
            coeff = variable.coeff * variable.expo * self.e.getDerivative(symbol)
            expo = variable.expo - 1
            new_e = variable.e
            return Variable(Sec(self.e), coeff = Variable(new_e, coeff = coeff, expo = expo),expo = 2)
    def convert(self):
        return Cot(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'tan({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class Csc(object):
    def __init__(self, e, name = 'csc'):
        self.e = e
        self.name = name
    def eval(self):
        try:
            return 1/sin(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return 1/sin(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf

    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            variable_coeff = Variable(Cot(self.e), coeff = -coeff)
            return Variable(Csc(self.e), coeff = variable_coeff)
        elif variable.expo > 1:
            coeff = variable.coeff * variable.expo * self.e.getDerivative(symbol)
            variable_coeff = Variable(Cot(self.e), coeff = -coeff)
            return Variable(Csc(self.e), coeff = variable_coeff, expo = variable.expo)
    def convert(self):
        return Sin(self.e)    
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'csc({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class Sec(object):
    def __init__(self, e, name = 'sec'):
        self.e = e
        self.name = name

    def eval(self):
        try:
            return 1/cos(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    def getCalc(self):
        try:
            return 1/cos(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf

    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            variable_coeff = Variable(Tan(self.e), coeff = coeff)
            return Variable(Sec(self.e), coeff = variable_coeff)
        elif variable.expo > 1:
            coeff = variable.coeff * variable.expo * self.e.getDerivative(symbol)
            variable_coeff = Variable(Tan(self.e), coeff = coeff)
            return Variable(Sec(self.e), coeff = variable_coeff, expo = variable.expo)
    def convert(self):
        return Cos(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'sec({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class Cot(object):
    def __init__(self, e, name = 'cot'):
        self.e = e
        self.name = name
    def eval(self):
        try:
            return 1/tan(self.e.eval())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    def getCalc(self):
        try:
            return 1/tan(self.e.getCalc())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            coeff = variable.coeff * self.e.getDerivative(symbol)
            return Variable(Csc(self.e), coeff = -coeff, expo = 2)
        elif variable.expo > 1:
            coeff = variable.coeff * variable.expo * self.e.getDerivative(symbol)
            expo = variable.expo - 1
            variable_coeff = Variable(Cot(self.e), coeff = -coeff, expo = expo)
            return Variable(Csc(self.e), coeff = variable_coeff,expo = 2)
    
    def convert(self):
        return Tan(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __repr__(self):
        return f'cot({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class ConstantE(object):
    def __init__(self, name = 'e'):
        self.e = E
        self.name = name
    def eval(self):
        return self.e
    
    def getCalc(self):
        return self.e

    def getDerivative(self, Variable, symbol):
        pass
    
    def convert(self):
        return self

    def __repr__(self):
        return self.name
class Pi(object):
    def __init__(self, name = 'pi'):
        self.e = PI
        self.name = name
    def eval(self):
        return self.e
    
    def getCalc(self):
        return self.e

    def getDerivative(self, Variable, symbol):
        pass
    
    def convert(self):
        return self
    
    def __repr__(self):
        return self.name
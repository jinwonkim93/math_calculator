from empty import Empty
from expression import Expr
import math
from mathematical_constant import PI, E
from utils import list2str, sortVariable
from copy import deepcopy


class Factor(object):
    def __init__(self, e, sign = Empty(), expo = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign
        self.expo = expo

    def canonicalize(self):
        return -self.expo.canonicalize(self.e.canonicalize()) if self.sign is '-' else self.expo.canonicalize(self.e.canonicalize())


    def eval(self):
        return -self.expo.eval(self.e.eval()) if self.sign is '-' else self.expo.eval(self.e.eval())

    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'


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

    def convertWhole(self):
        coeff = self.coeff
        expo = abs(self.expo)
        temp = Variable(self.e, expo = expo)
        molecular = coeff * temp
        parenthesis = self.e.getList()
        if len(parenthesis) == 1:
            parenthesis = parenthesis[0]
            parenthesis.expo = -parenthesis.expo
            return molecular * parenthesis
        else:
            parenthesis = self.e
            denominator = Variable(parenthesis, coeff = molecular, expo = -1)
            return denominator

    def __add__(self, other):
        if other == 0:return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = self.coeff + other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
        result = [self, "+", other]
        result = sortVariable(result)
        return Variable(Parenthesis(result))
    
    def __radd__(self, other):
        if other == 0: return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff + self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
        result = [self, "+", other]
        result = sortVariable(result)
        return Variable(Parenthesis(result))
    
    def __sub__(self,other):
        if other == 0: return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = self.coeff - other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
        result = [self, "-", other]
        result = sortVariable(result)
        return Variable(Parenthesis(result))    


    def __rsub__(self,other):
        if other == 0: return -self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff - self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
        return Variable(Parenthesis([other, "-", self]))
    
    def __mul__(self, other):
        if other == 0:return 0
        if self.expo == -0.5: self = self.convertWhole()
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                
                if coeff == 0:
                    return 0
                elif expo == 0:
                    return coeff
                else:
                    return Variable(self.e, coeff = coeff, expo = expo)
            
            elif self.e.__class__ == other.e.__class__:
                if self.e > other.e:
                    coeff = self.coeff * other
                    return Variable(self.e, coeff = coeff, expo = self.expo)
                else:
                    coeff = other.coeff * self
                    return Variable(other.e, coeff = coeff, expo = other.expo)
            
            elif isinstance(self.coeff, Variable):
                coeff = self.coeff * other
                return Variable(self.e, coeff = coeff, expo = self.expo)
            
            else:
                coeff = other.coeff * self
                return Variable(other.e, coeff = coeff, expo = other.expo)

        else:
            coeff = self.coeff * other
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
    
    def __rmul__(self, other):
        if other == 0:return 0
        if self.expo == -0.5: self = self.convertWhole()
        if isinstance(other, Variable):

            if self.e == other.e:
                coeff = self.coeff * other.coeff
                expo = self.expo + other.expo
                
                if coeff == 0:
                    return 0
                elif expo == 0:
                    return coeff
                else:
                    return Variable(self.e, coeff = coeff, expo = expo)
            
            elif self.e.__class__ == other.e.__class__:
                if self.e > other.e:
                    coeff = self.coeff * other
                    return Variable(self.e, coeff = coeff, expo = self.expo)
                else:
                    coeff = other.coeff * self
                    return Variable(other.e, coeff = coeff, expo = other.expo)
            
            elif isinstance(self.coeff, Variable):
                coeff = self.coeff * other
                return Variable(self.e, coeff = coeff, expo = self.expo)
            
            else:
                coeff = other.coeff * self
                return Variable(other.e, coeff = coeff, expo = other.expo)

        else:
            
            coeff = self.coeff * other
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
              
    def __truediv__(self, other):
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff / other.coeff
                expo = self.expo - other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if expo != 0 else coeff
            else:
                return self*Variable(other.e, coeff = other.coeff, expo = -other.expo)
        elif isinstance(other, Constant):
            coeff = self.coeff / other.canonicalize()
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
        else:
            coeff = self.coeff / other
            return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
    
    def __rtruediv__(self, other):
        if other == 0: 
            raise ZeroDivisionError
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
            value = other.canonicalize()
            coeff = value/self.coeff
            return Variable(self.e, coeff = coeff, expo = -self.expo).canonicalize()
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
        from fractions import Fraction
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
        
        e = self.e
        if isinstance(self.e, Parenthesis):
            temp = self.e.getList()
            if len(temp) == 1 and self.expo == 1:
                e = f'{e}'
            else:
                e = f'({e})'
        
        coeff = self.coeff
        if isinstance(coeff, (int,float)):
            coeff = Fraction(coeff).limit_denominator()
        if self.coeff != 1:
            if self.expo == 0:
                return f'{coeff}'
            
            elif self.expo < 0:
                return f'{coeff}*{e}^{self.expo}'
            elif self. expo == 1:
                return f'{coeff}*{e}'
            else:
                return f'{coeff}*{e}^{self.expo}'
        else:
            if self.expo == 0:
                return f'{coeff}'
            
            elif self.expo < 0:
                return f'{coeff}*{e}^{self.expo}'
            elif self. expo == 1:
                return f'{e}'
            else:
                return f'{e}^{self.expo}'
    
    def eval(self):
        if isinstance(self.e, Empty):
            res = self.coeff**self.expo
            res = self.coeff * res
            return res
        if isinstance(self.e, (int,float)):
            res = self.e ** self.expo
            res = self.coeff * res
            return res
        else:
            res = self.e.eval()**self.expo
            res = self.coeff * res
            return res
    
    def canonicalize(self):
        res = None
        if isinstance(self.e, Parenthesis):
            temp = self.e.getList()
            if len(temp) == 1:
                return temp[0]
        
        if isinstance(self.e, float):
            return self.e
        else:
            if not isinstance(self.e, (int,float,Symbol,Empty)):
                self.e = self.e.canonicalize()
                if isinstance(self.expo, Variable):
                    return self
                elif self.expo < 0:
                    self.e = self.e.convert()
                    self.expo = -self.expo
            return self if self.coeff != 0 else 0


    def getDerivative(self, symbol):
        if isinstance(self.e, (int,float)): return 0
        
        elif isinstance(self.expo, Variable):
            res_variable = 0
            if isinstance(self.coeff, Variable):
                coeff = self.coeff.getDerivative(symbol)
                coeff = coeff*Variable(self.e, expo = self.expo)
                res_variable += coeff
            fx = deepcopy(self)
            log_val = Log(E,self.e).canonicalize() if isinstance(self.e, ConstantE) else Log(E,self.coeff)
            temp_variable = Variable(log_val) if isinstance(log_val, Log) else log_val 
            expo_derivative = self.expo.getDerivative(symbol)
            res_variable += fx  * temp_variable * expo_derivative
            return res_variable
                
        elif isinstance(self.e, Empty):
            if self.coeff == E:
                expo = self.expo.getDerivative(symbol)
                return Variable(Empty(),coeff = self.coeff, expo = expo)
            else:
                return 0
        
        elif isinstance(self.e, (Sin,Cos,Tan,Sec,Cot,Csc, Log, Symbol, Variable)):
            coeff = self.coeff
            res_variable = 0

            
            if isinstance(self.coeff, Variable):
                coeff = coeff.getDerivative(symbol)
                coeff = coeff*Variable(self.e, expo = self.expo)
                res_variable += coeff
            
            derivative, inner_derivative = self.e.getDerivative(symbol)
            if derivative == 0 and not isinstance(coeff, Variable): return 0
            
            temp_variable1 = derivative
            temp_variable2 = Variable(self.e, expo = self.expo-1) if self.expo-1 != 0 else 1
            
            
            if isinstance(inner_derivative, list):
                for idx in range(0,len(inner_derivative), 2):
                    element = inner_derivative[idx]
                    temp_variable = element * self.coeff * self.expo * temp_variable1 * temp_variable2 
                    res_variable += temp_variable

            else:
                res_variable += temp_variable1*inner_derivative*temp_variable2*self.expo*self.coeff 
            
            return res_variable
        elif isinstance(self.e, Parenthesis) and self.expo < 0:
            return Variable(self.e, coeff = self.coeff*self.expo , expo = self.expo-1)
        elif isinstance(self.e, Parenthesis) and self.expo > 0 and self.expo < 1:
            coeff = self.expo
            expo = self.expo - 1
            fx = Variable(self.e, expo = expo)
            inner_derivative = self.e.getDerivative(symbol)
            inner_derivative = [coeff*x for x in inner_derivative]
            if len(inner_derivative) == 1:
                inner_derivative = inner_derivative[0]
            elif len(inner_derivative) == 0: return 0
            else:
                inner_derivative = Variable(Parenthesis(inner_derivative))    
            return inner_derivative * fx
        else:
            return self.e.getDerivative(symbol)



class Symbol(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.value = None

        
    def insert(self, value):
        self.value = float(value)
    
    def canonicalize(self):
        return self
    
    def eval(self):
        return self.value
    
    def getDerivative(self, symbol):
        if self == symbol: return 1, 1
        else: return 0, 0
    
    def __lt__(self, other):
        return self.__class__ == other.__class__ and self.symbol < other.symbol
    # def __gt__(self, other):
    #     return self.__class__ == other.__class__ and self.symbol > other.symbol
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
    
    def canonicalize(self):
        return self.expo.canonicalize(self.value)
    
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

from math import sin, cos, tan
import numpy as np

class Log(object):
    def __init__(self, symbol, e, name = 'log'):
        self.symbol = float(symbol)
        self.e = e
        self.name = name
    
    def canonicalize(self):
        try:
            e_val = self.e.canonicalize() if isinstance(self.e, Variable) else self.e
            if isinstance(self.e, ConstantE): e_val = self.e.eval() 
            return self.lognNew(e_val,self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
        except TypeError:
            return self
    
    def eval(self):
        try:
            return self.lognNew(self.e.eval(),self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
    
    def lognNew(self, n, x = E):
        return math.log(n) / math.log(x)
    
    def getDerivative(self,symbol):
        df = self.e.getDerivative(symbol)
        numerator = self.e.canonicalize()
        if df == 0:
            return 0, 0
        else:
            if isinstance(numerator, list):
                numerator = Variable(Parenthesis(numerator),expo = -1)    
                if E == self.symbol:
                    return numerator, df
                return numerator*Variable(Log(E,self.symbol), expo = -1), df
            return 1/numerator, df


    def convert(self):
        return self
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    
    def __str__(self):
        return f'log{str(self.symbol):.4}({str(self.e)})'
    
    def __repr__(self): 
        return f'Log({repr(self.symbol)},{self.e})'

class Sin(object):
    def __init__(self,e, name = 'sin'):
        self.e = e
        self.name = name
    
    def canonicalize(self):
        try:
            return sin(self.e.canonicalize())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def eval(self):
        try:
            return sin(self.e.eval())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, symbol):
        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return Variable(Cos(self.e)), df
    
    def convert(self):
        return Csc(self.e)
    
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)

    def __repr__(self):
        return f'sin({list2str(self.e.canonicalize())})'

class Cos(object):
    def __init__(self, e, name = 'cos'):
        self.e = e
        self.name = name

    def canonicalize(self):
        try:
            return cos(self.e.canonicalize())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def eval(self):
        try:
            return cos(self.e.eval())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, symbol):
        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return -Variable(Sin(self.e)), df

    
    def convert(self):
        return Sec(self.e)

    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'cos({self.e})' if isinstance(self.e.canonicalize(), (list, Variable)) else f'{self.e.canonicalize()}'

class Tan(object):
    def __init__(self, e, name = 'tan'):
        self.e = e
        self.name = name
    
    def canonicalize(self):
        try:
            res = tan(self.e.canonicalize())
            if res > 10E15: res = np.inf
            if res < -10E15: res = -np.inf
            return res
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def eval(self):
        try:
            res = tan(self.e.eval())
            if res > 10E15: res = np.inf
            if res < -10E15: res = -np.inf
            return res
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, symbol):

        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return Variable(Sec(self.e), expo = 2), df
    
    def convert(self):
        return Cot(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'tan({self.e})' if isinstance(self.e.canonicalize(), (list, Variable)) else f'{self.e.canonicalize()}'

class Csc(object):
    def __init__(self, e, name = 'csc'):
        self.e = e
        self.name = name
    def canonicalize(self):
        try:
            return 1/sin(self.e.canonicalize())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    
    def eval(self):
        try:
            return 1/sin(self.e.eval())
        except ZeroDivisionError:
            return np.inf


    def getDerivative(self, symbol):
        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return -Variable(Cot(self.e))*Variable(Csc(self.e)), df
    def convert(self):
        return Sin(self.e)    
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'csc({self.e})' if isinstance(self.e.canonicalize(), (list, Variable)) else f'{self.e.canonicalize()}'

class Sec(object):
    def __init__(self, e, name = 'sec'):
        self.e = e
        self.name = name

    def canonicalize(self):
        try:
            return 1/cos(self.e.canonicalize())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    def eval(self):
        try:
            return 1/cos(self.e.eval())
        except ZeroDivisionError:
            return np.inf

    def getDerivative(self, symbol):
        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return Variable(Tan(self.e))*Variable(Sec(self.e)), df
    
    def convert(self):
        return Cos(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'sec({self.e})' if isinstance(self.e.canonicalize(), (list, Variable)) else f'{self.e.canonicalize()}'

class Cot(object):
    def __init__(self, e, name = 'cot'):
        self.e = e
        self.name = name
    def canonicalize(self):
        try:
            return 1/tan(self.e.canonicalize())
        except ZeroDivisionError:
            return np.inf
        except TypeError:
            return self
    def eval(self):
        try:
            return 1/tan(self.e.eval())
        except ZeroDivisionError:
            return np.inf
    
    def getDerivative(self, symbol):
        df = self.e.getDerivative(symbol)
        if df == 0:
            return 0, 0
        else:
            return -Variable(Csc(self.e),expo = 2), df
    
    def convert(self):
        return Tan(self.e)
    def __eq__(self,other):
        if self.__class__ == other.__class__ and repr(self.e) == repr(other.e):return True
        else: return False
    def __lt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'cot({self.e})' if isinstance(self.e.canonicalize(), (list, Variable)) else f'{self.e.canonicalize()}'

class ConstantE(object):
    def __init__(self, name = 'e'):
        self.e = E
        self.name = name
    
    def canonicalize(self):
        return self
    
    def eval(self):
        return self.e

    def getDerivative(self, Variable, symbol):
        pass
    
    def convert(self):
        return self

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Pi(object):
    def __init__(self, name = 'pi'):
        self.e = PI
        self.name = name
    def canonicalize(self):
        return self.e
    
    def eval(self):
        return self.e

    def getDerivative(self, Variable, symbol):
        pass
    
    def convert(self):
        return self
    
    def __repr__(self):
        return self.name

class Parenthesis(object):
    def __init__(self, e, name = 'Parenthesis'):
        self.e = e
        self.name = name
    
    def getList(self):
        return self.e
    
    def eval(self):
        temp = []
        res = 0
        op = '+'
        for idx in range(0,len(self.e),2):
            element = self.e[idx]
            if idx > 0:
                op = self.e[idx-1]
            if isinstance(element, Variable):
                element = element.eval()
            res = calc(op,res,element)                
        return res
        
    def getDerivative(self, symbol):
        temp = []
        semi_expression = self.getList()
        if isinstance(semi_expression, list):
            for value in semi_expression:
                if isinstance(value, (int,float)):
                    if len(temp) > 0: temp.pop()
                    temp.append(0)

                elif value in ('+', '-', '*', '/'):
                    temp.append(value)                            
                else:
                    derivation = value.getDerivative(symbol)
                    if isinstance(derivation, (int,float)):
                        if derivation == 0:
                            if len(temp) > 0: temp.pop()
                        else:
                            if len(temp) == 1: temp.pop()
                            temp.append(derivation)
                    else:
                        if derivation.coeff == 0:
                            if len(temp) > 0: temp.pop()
                        else:
                            if len(temp) == 1: temp.pop()
                            temp.append(derivation)
            return temp
    def __eq__(self, other):
        if self.__class__ != other.__class__: return False
        return list2str(self.e) == list2str(other.e)
    def __lt__(self, other):
        if self.__class__ != other.__class__: return False
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if self.__class__ != other.__class__: return False
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'{list2str(self.e)}'

def calc(op, left, right):
    if op is '+':
        return left + right
    elif op is '-':
        return left - right
    elif op is '*':
        return left * right
    elif op is '/':
        return left / right
#from node import Node
from empty import Empty
from expression import Expr
import math
from mathematical_constant import PI, E
# from utils import clearExpr
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
        if other == 0:return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = self.coeff + other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            
            if isinstance(self.expo, Variable):
                return Variable(Parenthesis([other, "+", self]))
            if other.expo > self.expo:
                return Variable(Parenthesis([other, "+", self]))
            elif other.e < self.e:
                return Variable(Parenthesis([other, '+', self]))
            
        return Variable(Parenthesis([self, "+", other]))
    
    def __radd__(self, other):
        if other == 0: return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff + self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [other, "+", self]
        return Variable(Parenthesis([other, "+", self]))
    
    def __sub__(self,other):
        if other == 0: return self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = self.coeff - other.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [-other, "+", self]
        return Variable(Parenthesis([self, "-", other]))

    def __rsub__(self,other):
        if other == 0: return -self
        if isinstance(other, Variable):
            if self.checkVariable(self,other):
                coeff = other.coeff - self.coeff
                return Variable(self.e, coeff = coeff, expo = self.expo) if coeff != 0 else 0
            if other.expo > self.expo:
                return [other, "-", self]
            else:
                return [-self, '+', other]
        return Variable(Parenthesis([other, "-", self]))
    
    def __mul__(self, other):
        if other == 0:return 0
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
    
    # def __rmul__(self, other):
    #     if other == 0: return 0
    #     if isinstance(other, Variable):
    #         if self.e == other.e:
    #             coeff = self.coeff * other.coeff
    #             expo = self.expo + other.expo
    #             return Variable(self.e, coeff = coeff, expo = expo) if coeff is not 0 else 0
    #         else:
    #             return [self, "*", other]
    #     elif isinstance(other, Constant):
    #         coeff = other.eval() * self.coeff
    #         return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
    #     else:
    #         coeff = other * self.coeff
    #         return Variable(self.e, coeff = coeff, expo = self.expo) if coeff is not 0 else 0
              
    def __truediv__(self, other):
        if isinstance(other, Variable):
            if self.e == other.e:
                coeff = self.coeff / other.coeff
                expo = self.expo - other.expo
                return Variable(self.e, coeff = coeff, expo = expo) if expo != 0 else coeff
            else:
                return self*Variable(other.e, coeff = other.coeff, expo = -other.expo)
                #return [self, "/", other]
        elif isinstance(other, Constant):
            coeff = self.coeff / other.eval()
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
            fx = deepcopy(self)
            #log_val = Log(E,self.coeff).eval()
            log_val = Log(E,self.e).eval()
            temp_variable = Variable(log_val) if isinstance(log_val, Log) else log_val 
            expo_derivative = self.expo.getDerivative(symbol)
            return fx  * temp_variable * expo_derivative
                
        elif isinstance(self.e, Empty):
            if self.coeff == E:
                expo = self.expo.getDerivative(symbol)
                return Variable(Empty(),coeff = self.coeff, expo = expo)
            else:
                return 0
        
        elif isinstance(self.e, (Sin,Cos,Tan,Sec,Cot,Csc, Log, Symbol)):
            derivative, inner_derivative = self.e.getDerivative(symbol)
            coeff = self.coeff
            res_variable = 0
            
            if isinstance(self.coeff, Variable):
                coeff = coeff.getDerivative(symbol)
                coeff = coeff*Variable(self.e, expo = self.expo)
                res_variable += coeff
            
            if derivative == 0: return 0
            temp_variable1 = derivative
            temp_variable2 = Variable(self.e, expo = self.expo-1)
            
            
            if isinstance(inner_derivative, list):
                for idx in range(0,len(inner_derivative), 2):
                    element = inner_derivative[idx]
                    # print('self.e', self.e)
                    # print('element = ', element)
                    # print('self.coeff = ', self.coeff)
                    # print('self.expo = ', self.expo)
                    # print('temp_variable1 = ', temp_variable1)
                    # print('temp_variable2 = ', temp_variable2)
                    temp_variable = element * self.coeff * self.expo * temp_variable1 * temp_variable2 
                    res_variable += temp_variable

            else:
                # print('self.e', self.e)
                # print('inner_derivative = ', inner_derivative)
                # print('self.coeff = ', self.coeff)
                # print('self.expo = ', self.expo)
                # print('temp_variable1 = ', temp_variable1)
                # print('temp_variable2 = ', temp_variable2)
                res_variable += temp_variable1*inner_derivative*temp_variable2*self.expo*self.coeff
            
            return res_variable

        elif isinstance(self.e, Parenthesis) and self.expo < 0:
            return Variable(self.e, coeff = self.coeff*self.expo , expo = self.expo-1)

        else:
            return self.e.getDerivative(symbol)
            # return 0
            # return self.e.getDerivative(self,symbol)



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
    
    def getDerivative(self, symbol):
        if self == symbol: return 1, 1
        else: return 0, 0
    
    def __lt__(self, other):
        return self.__class__ == other.__class__ and self.symbol < other.symbol
    def __gt__(self, other):
        return self.__class__ == other.__class__ and self.symbol > other.symbol
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
        return self.expo.eval(self.value)
    
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
        self.symbol = float(symbol)
        self.e = e
        self.name = name
    
    def eval(self):
        try:
            # return self.lognNew(self.e.eval(),self.symbol)
            e_val = self.e.eval() if isinstance(self.e, Variable) else self.e
            if isinstance(self.e, ConstantE): e_val = self.e.getCalc() 
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
    
    def getDerivative(self,symbol):
        df = self.e.getDerivative(symbol)
        numerator = self.e.eval()
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
        """ e_val = self.e.eval()
        if isinstance(e_val, Variable):
            self.e = "집가서하자"
            coeff = e_eval.expo

            return Variable(,)"""
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
        return f'sin({list2str(self.e.eval())})'

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
        return repr(self.e) > repr(other.e)
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
        return f'cot({self.e})' if isinstance(self.e.eval(), (list, Variable)) else f'{self.e.eval()}'

class ConstantE(object):
    def __init__(self, name = 'e'):
        self.e = E
        self.name = name
    
    def eval(self):
        return self
    
    def getCalc(self):
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

class Parenthesis(object):
    def __init__(self, e, expo = 1, name = 'Parenthesis'):
        self.e = e
        self.expo = expo
        self.name = name
    
    def getList(self):
        return self.e
    
    def getCalc(self):
        temp = []
        res = 0
        op = '+'
        for idx in range(0,len(self.e),2):
            element = self.e[idx]
            if idx > 0:
                op = self.e[idx-1]
            if isinstance(element, Variable):
                element = element.getCalc()
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
        if isinstance(other, Symbol): return True
        return repr(self.e) < repr(other.e)
    def __gt__(self, other):
        if isinstance(other, Symbol): return True
        return repr(self.e) > repr(other.e)
    def __repr__(self):
        return f'{list2str(self.e)}' if self.expo == 1 else f'({list2str(self.e)})^{self.expo}'
        #return f'({self.e})'

def calc(op, left, right):
    if op is '+':
        # print(left, '+', right)
        return left + right
    elif op is '-':
        # print(left, '-', right)
        return left - right
    elif op is '*':
        # print(left, '*', right)
        return left * right
    elif op is '/':
        # print(left, '/', right)
        return left / right
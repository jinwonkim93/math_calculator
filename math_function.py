from expression import Expr
from empty import Empty
from utils import lognNew, isExpr
from factor_new import Variable, Constant
from math import sin, cos, tan
from mathematical_constant import PI
import numpy as np

class Log(object):
    def __init__(self, symbol, e, name = 'log'):
        super(__class__,self)
        self.symbol = float(symbol)
        self.e = e
        self.name = name
    
    def eval(self):
        try:
            return lognNew(self.e.eval(),self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
        except TypeError:
            return self
    
    def getCalc(self):
        try:
            return lognNew(self.e.getCalc(),self.symbol)
        except ZeroDivisionError:
            return np.inf
        except ValueError:
            return np.nan
    
    def getDerivative(self, variable, symbol):
        if isinstance(self.e, (int,float)): return NotImplemented
        if variable.expo == 1:
            e_val = self.e.eval()
            coeff = variable.coeff * self.e.getDerivative(symbol)
            print(e_val, type(e_val))
            if isinstance(e_val, Variable):
                coeff = coeff/e_val
                return Variable(self,coeff = coeff, expo = variable.expo)
                # return coeff / e_val
            else:
                return [coeff, '/', e_val]
        elif variable.expo > 1:
            coeff = variable.expo * variable.coeff * self.e.getDerivative(symbol)
            return Variable(self,coeff = coeff, expo=variable.expo-1) / self.e.eval()
    
    def convert(self):
        """ e_val = self.e.eval()
        if isinstance(e_val, Variable):
            self.e = "집가서하자"
            coeff = e_eval.expo

            return Variable(,)"""
        return self
    
    def __str__(self):
        return f'log{str(self.symbol):.4}({str(self.e)})'
    def __repr__(self):
        return f'Log({repr(self.symbol)},{repr(self.e)})'

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
import math
from node import Node
from expression import Expr
from empty import Empty
from mathematical_constant import *
from factor import Variable, Constant

class AngleFunction(Node):
    def __init__(self, angleF, e):
        super(__class__,self)
        self.angleF = angleF
        self.e = e
    def eval(self):
        return triangleFunction(self.angleF, self.e.eval())
    
    def __str__(self):
        return f'{str(self.angleF)}({str(self.e)})'
    def __repr__(self):
        return f'AngleFunction({repr(self.angleF)},{repr(self.e)})'

class Exponential(Node):
    def __init__(self, f, expo):
        super(__class__,self)
        self. f = f
        self.expo = expo
    
    def eval(self, left):
        eval_factor = self.expo.eval(self.f.eval())
        try:
            return left**eval_factor
        except:
            raise Exception("OverflowError: Numerical result out of range")

            
    def __str__(self):
        if isinstance(self.expo, Empty):
            return f'^({str(self.f)})' if isinstance(self.f, Expr) else f'^{str(self.f)}'
        else:
            return f'^({str(self.f)})^{str(self.expo)}' if isinstance(self.f, Expr) else f'^{str(self.f)}{str(self.expo)}'
    def __repr__(self):
        return f'Exponential({repr(self.f)},{repr(self.expo)})'

class Log(Node):
    def __init__(self, logarithm, e):
        super(__class__,self)
        self.logarithm = logarithm
        self.e = e
    
    def eval(self):
        return lognNew(self.e.eval(),self.logarithm)
        
    def __str__(self):
        return f'log{str(self.logarithm):.4}({str(self.e)})'
    def __repr__(self):
        return f'Log({repr(self.logarithm)},{repr(self.e)})'

def logn(n, x = math.e):
    print(n/x)
    return 1 + logn(n/x, x) if n > (x-1) else 0

def lognNew(n, x = E):
    return math.log(n) / math.log(x)

def triangleFunction(func, expr):
    if func == 'sin':
        return math.sin(expr)
    elif func == 'cos':
        return math.cos(expr)
    elif func == 'tan':
        return math.tan(expr)

def pow(base,expo):
    if isinstance(base, Variable):
        base.expo = base.expo ** expo
        return base
    elif isinstance(base, Constant):
        return base.e ** expo
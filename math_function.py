import math
from node import Node
from expression import Expr
from empty import Empty
from mathematical_constant import *

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

from node import Node
from expression import Expr
from empty import Empty
from utils import lognNew, triangleFunction


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


from node import Node
from empty import Empty


class Expr(Node):
    def __init__(self, t, et):
        super(__class__,self)
        self.t = t
        self.et = et
    
    def eval(self):
        result = self.et.eval(self.t.eval())
        return result
    def getCalc(self):
        result = self.et.getCalc(self.t.getCalc())
        return result
    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'



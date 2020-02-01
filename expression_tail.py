from node import Node
from utils import calcByTerm, calc

class ExprTail(Node):
    def __init__(self, op, t, et):
        super(__class__,self)
        self.op = op
        self.t = t
        self.et = et
    

    def eval(self, left):
        eval_term = self.t.eval()
        #left = self.calc(left, eval_term)
        left = calcByTerm(self.op, left, eval_term)
        return self.et.eval(left)
    def getCalc(self, left):
        eval_term = self.t.getCalc()
        # left = calcByTerm(self.op, left, eval_term)
        left = calc(self.op, left, eval_term)
        return self.et.getCalc(left)
    def __str__(self):
        return f'{str(self.op)}{str(self.t)}{str(self.et)}'
    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.t)}, {repr(self.et)})'
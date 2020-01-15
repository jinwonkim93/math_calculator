from node import Node
from empty import Empty

class Expr(Node):
    def __init__(self, t, et):
        super(__class__,self)
        self.t = t
        self.et = et
    
    def eval(self):
        return self.et.eval(self.t.eval())

    def canonicalize(self):
        term = []
        constant = None
        seq = self.et.canonicalize(self.t.canonicalize([term,constant]))
    
    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'

class ExprTail(Node):
    def __init__(self, op, t, et):
        super(__class__,self)
        self.op = op
        self.t = t
        self.et = et
    

    def eval(self, left):
        eval_term = self.t.eval()
        #left = self.calc(left, eval_term)
        left = self.calcByTerm(left, eval_term, self.checkTerm)
        return self.et.eval(left)

    def canonicalize(self, seq):
        pass

    def checkTerm(self, left,right):
        if isinstance(left,right.__class__):
            if isinstance(left, Constant):
                return True
            else:
                if left.expo == right.expo:
                    return True
                else:
                    return False
        else:
            return False

    def __str__(self):
        return f'{str(self.op)}{str(self.t)}{str(self.et)}'
    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.t)}, {repr(self.et)})'
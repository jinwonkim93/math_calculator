from node import Node
from empty import Empty


class Expr(Node):
    def __init__(self, t, et):
        super(__class__,self)
        self.t = t
        self.et = et
    
    def eval(self):
        result = self.et.eval(self.t.eval())
        if isinstance(result, list):
            [x for x in result]
        #return  ''.join(list(map(str,result))) if isinstance(result,list) else result
        return result

    def canonicalize(self):
        term = []
        constant = None
        seq = self.et.canonicalize(self.t.canonicalize([term,constant]))
    
    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'


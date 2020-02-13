from calculator import calcByTerm, calc

class ExprTail(object):
    def __init__(self, op, t, et):
        self.op = op
        self.t = t
        self.et = et
    

    def canonicalize(self, left):
        canonicalize_term = self.t.canonicalize()
        left = calcByTerm(self.op, left, canonicalize_term)
        return self.et.canonicalize(left)
    def eval(self, left):
        canonicalize_term = self.t.eval()
        left = calc(self.op, left, canonicalize_term)
        return self.et.eval(left)
    def __str__(self):
        return f'{str(self.op)}{str(self.t)}{str(self.et)}'
    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.t)}, {repr(self.et)})'
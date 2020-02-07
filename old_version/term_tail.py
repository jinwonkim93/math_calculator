from calculator import calcByTerm, calc
import numpy as np
class TermTail(object):
    def __init__(self, op, f,  tt):
        self.op = op
        self.f = f
        self.tt = tt
    
    def canonicalize(self, left):
        return self.tt.canonicalize(self.merge(left.canonicalize(), self.f.canonicalize()))

    def merge(self, factors, factor):
        # for left_factor in factors:
        merged = []

        for i in range(len(factors)):
            compare = factors[i].comparePrecedence(factor)
            if compare > 0:
                merged.append(factor)
                merged.append(factors[i])
            elif compare == 0:
                merged.append(factors[i].merge(factor))
            else:
                merged.append(factors[i])

        return merged
    
    def canonicalize(self, left):
        try:
            canonicalize_factor = self.f.canonicalize()
            left = calcByTerm(self.op, left,canonicalize_factor)
            return self.tt.canonicalize(left)
        except ZeroDivisionError:
            return np.inf
    def eval(self, left):
        try:
            canonicalize_factor = self.f.eval()
            # left = calcByTerm(self.op, left,canonicalize_factor)
            left = calc(self.op, left,canonicalize_factor)
            return self.tt.eval(left)
        except ZeroDivisionError:
            return np.inf

    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.tt)})'
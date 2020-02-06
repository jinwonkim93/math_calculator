from calculator import calcByTerm, calc
import numpy as np
class TermTail(object):
    def __init__(self, op, f,  tt):
        self.op = op
        self.f = f
        self.tt = tt
    
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
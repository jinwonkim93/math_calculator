from empty import Empty
from expression import Expr
from factor import Symbol, Constant
from calculator import pow

class FactorTail(object):
    def __init__(self, f, expo):
        self. f = f
        self.expo = expo
    
    def canonicalize(self, left):
        canonicalize_factor = self.expo.canonicalize(self.f.canonicalize())
        try:
            return pow(left,canonicalize_factor)
        except Exception as e:
            raise e
    def eval(self,left):
        canonicalize_factor = self.expo.eval(self.f.eval())
        try:
            return pow(left,canonicalize_factor)
        except:
            raise Exception("OverflowError: Numerical result out of range")
    def __str__(self):
        if isinstance(self.expo, Empty):
            return f'^({str(self.f)})' if isinstance(self.f, Expr) else f'^{str(self.f)}'
        else:
            return f'^({str(self.f)})^{str(self.expo)}' if isinstance(self.f, Expr) else f'^{str(self.f)}{str(self.expo)}'
    def __repr__(self):
        return f'FactorTail({repr(self.f)},{repr(self.expo)})'
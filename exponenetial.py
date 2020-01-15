from node import Node
from empty import Empty
from factor import Symbol, Constant
from math_function import pow

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

    def canonicalize(self, left):
        #지수함수에 변수 안됌 아직
        canonicalized_factor = self.expo.canonicalize(self.f.eval())
        left = pow(left,canonicalized_factor)
        return left


    def __str__(self):
        if isinstance(self.expo, Empty):
            return f'^({str(self.f)})' if isinstance(self.f, Expr) else f'^{str(self.f)}'
        else:
            return f'^({str(self.f)})^{str(self.expo)}' if isinstance(self.f, Expr) else f'^{str(self.f)}{str(self.expo)}'
    def __repr__(self):
        return f'Exponential({repr(self.f)},{repr(self.expo)})'
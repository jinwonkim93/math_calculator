from node import Node
from empty import Empty

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

            
    def __str__(self):
        if isinstance(self.expo, Empty):
            return f'^({str(self.f)})' if isinstance(self.f, Expr) else f'^{str(self.f)}'
        else:
            return f'^({str(self.f)})^{str(self.expo)}' if isinstance(self.f, Expr) else f'^{str(self.f)}{str(self.expo)}'
    def __repr__(self):
        return f'Exponential({repr(self.f)},{repr(self.expo)})'
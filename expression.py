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
    
    def getDerivative(self, symbol):
            semi_expression = self.eval()
            temp = []
            if isinstance(semi_expression, list):
                for value in semi_expression:
                    if isinstance(value, (int,float)):
                        if len(temp) > 0: temp.pop()
                    elif value in ('+', '-', '*', '/'):
                        temp.append(value)
                    else:
                        derivation = value.getDerivative(symbol)
                        if derivation == 0:
                            if len(temp) > 0: temp.pop()
                        else:
                            if len(temp) == 1: temp.pop()
                            temp.append(derivation)

                d = ''
                if len(temp) == 1: return temp[0] #하나면 숫자를 두개 이상이면 str
                for element in temp:
                    d += str(element)
                return d
            else:
                if isinstance(semi_expression, (int,float)):
                    return NotImplemented
                else:
                    return semi_expression.getDerivative(symbol)
    
    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'



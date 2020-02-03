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
        try:
            temp = []
            if isinstance(semi_expression, list):
                for value in semi_expression:
                    if isinstance(value, (int,float)):
                        if len(temp) > 0: temp.pop()
                        temp.append(0)

                    elif value in ('+', '-', '*', '/'):
                        temp.append(value)                            
                    else:
                        derivation = value.getDerivative(symbol)
                        if isinstance(derivation, (int,float)):
                            if derivation == 0:
                                if len(temp) > 0: temp.pop()
                            else:
                                if len(temp) == 1: temp.pop()
                                temp.append(derivation)
                        else:
                            if derivation.coeff == 0:
                                if len(temp) > 0: temp.pop()
                            else:
                                if len(temp) == 1: temp.pop()
                                temp.append(derivation)

                return temp
            else:
                if isinstance(semi_expression, (int,float)):
                    return 0
                else:
                    derivation = semi_expression.getDerivative(symbol)
                    return derivation
                
        except Exception as e:
            raise e
            #return semi_expression
            
    def expr2str(self,expr):
        try:
            d = ''
            for value in expr:
                if isinstance(value, list):
                    value = self.expr2str(value)
                d += str(value)
            
            return d
        except:
            return str(expr)

    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'



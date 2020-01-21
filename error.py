class Error(object):
    def __init__(self,error):
        self.error = error
    
    def __str__(self):
        return "Error"
    
    def __repr__(self):
        return "Error(Expr)"
    
    def eval(self):
        return self.error
    def getCalc(self):
        return self.error
    def getDerivative(self, symbol):
        return self.error
class Error(object):
    def __init__(self,error):
        self.error = error
    
    def __str__(self):
        return "Error"
    
    def __repr__(self):
        return "Error(Expr)"
    
    def canonicalize(self):
        return self.error
    def eval(self):
        return self.error
    def getDerivative(self, symbol):
        return self.error

class NonDerivableError(object):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return f'{self.value} is not derivable'
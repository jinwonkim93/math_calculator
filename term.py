class Term(object):
    def __init__(self, f, tt):
        self.f = f
        self.tt = tt
    
    def eval(self):
        return self.tt.eval(self.f.eval())
    def getCalc(self):
        return self.tt.getCalc(self.f.getCalc())

    def getDerivative(self):
        pass
    def __str__(self):
        return f'{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.tt)})'
        

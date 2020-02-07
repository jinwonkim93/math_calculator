class Term(object):
    def __init__(self, f, tt):
        self.f = f
        self.tt = tt
    
    def canonicalize(self):
        return self.tt.canonicalize(self.f.canonicalize()))


        
    def eval(self):
        return self.tt.eval(self.f.eval())

    def getDerivative(self):
        pass
    def __str__(self):
        return f'{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.tt)})'
        

# x * y * x^2


# (x) * y * x^2
# (x * y) * x^2
# (x^3 * y)
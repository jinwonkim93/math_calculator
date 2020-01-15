from node import Node
class Term(Node):
    def __init__(self, f, tt):
        super(__class__,self)
        self.f = f
        self.tt = tt
    
    def eval(self):
        return self.tt.eval(self.f.eval())
    
    def canonicalize(self, seq):
        term = list(seq[0])
        constant = seq[1]

        return self.tt.canonicalize(self.f.canonicalize())

    def __str__(self):
        return f'{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.tt)})'
        

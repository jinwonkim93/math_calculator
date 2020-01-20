class Empty(object):
    def __init__(self):
        self.symbol = ''
    def __repr__(self):
        return 'Empty'
    
    def eval(self, left):
        return left
    def getCalc(self, left):
        return left
    def canonicalize(self, left):
        return left

    def __str__(self):
        return ''
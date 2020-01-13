class Empty(object):
    def __repr__(self):
        return 'Empty'
    
    def eval(self, left):
        return left
    
    def __str__(self):
        return ''
import re
from collections.abc import Iterable
from mathematical_constant import greeks, E, PI

class Scanner(object):
    def __init__(self, line):
        self.tokens = re.findall(r'[-+]|[a-z|A-Z]+|[0-9]*\.?[0-9]+|[*+-/()^]', line) + ['EOL']
        
    def peak(self):
        if len(self.tokens):
            return self.tokens[0]
        else:
            raise Exception("Empty Tokens, check Expression")
    
    def shift(self):
        if len(self.tokens):
            return self.tokens.pop(0)
        else:
            raise Exception("Empty Tokens, check Expression")
    
    def takeIt(self, tokenType = None):
        if tokenType is None or self.isType(tokenType):
            return self.shift()
        else:
            raise Exception("Expected: %s, Actual: %s" % (tokenType.__name__, self.peak()))
        
    def isType(self, tokenType):
        if callable(tokenType):
            return tokenType(self.peak())
        
        elif isinstance(tokenType, Iterable):
            return self.peak() in tokenType
        
        else:
            return False
    
    def isDigit(self, value):
        if value in greeks: return True
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def isAlpha(self, value):
        if value in greeks: return False
        return value.isalpha()

    def isSpecialNum(self, value):
        if value == 'e': return E
        if value == 'pi': return PI
        else: return value
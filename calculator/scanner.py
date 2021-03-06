import re
from collections.abc import Iterable
from calculator.mathematical_constant import greeks

class Scanner(object):
    def __init__(self, line):
        line = line.replace(' ', '').lower()
        self.tokens = re.findall(r'[-+]|[a-zA-Z]+|[0-9]*\.?[0-9]+|[*+-/()^,]', line) + ['EOL']
        print(self.tokens)
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
            raise Exception("Expected: %s, Actual: %s" % (tokenType, self.peak()))
        
    def isType(self, tokenType):
        if callable(tokenType):
            return tokenType(self.peak())
        
        elif isinstance(tokenType, Iterable):
            return self.peak() in tokenType
        
        else:
            return False
    def isFunction(self,value):
        functionDict = {'sin': True,
                        'cos': True,
                        'log': True}
        return functionDict.get(value,False)

    def isDigit(self, value):
        if value in greeks: return False
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def isAlpha(self, value):
        if value in greeks: return True
        return value.isalpha()

    def isSpecialNum(self, value):
        if value in greeks: return True
class Node(object):
    def __init__(self, op):
        self.op = op
    def calc(self, left, right):
        if self.op is '+':
            return left + right
        elif self.op is '-':
            return left - right
        elif self.op is '*':
            return left * right
        elif self.op is '/':
            return left / right

        
class Empty(object):
    def __repr__(self):
        return 'Empty'
    
    def eval(self, left):
        return left
    
class Expr(Node):
    def __init__(self, t, et):
        super(__class__,self)
        self.t = t
        self.et = et
    
    def eval(self):
        return self.et.eval(self.t.eval())

    
    def __repr__(self):
        return f'Expr({self.t}, {self.et})'
    
class ExprTail(Node):
    def __init__(self, op, t, et):
        super(__class__,self)
        self.op = op
        self.t = t
        self.et = et
    
    def eval(self, left):
        eval_term = self.t.eval()
        left = self.calc(left, eval_term)
        return self.et.eval(left)

    
    def __repr__(self):
        return f'ExprTail({self.op}, {self.t}, {self.et})'


class Term(Node):
    def __init__(self, f, tt):
        super(__class__,self)
        self.f = f
        self.tt = tt
    
    def eval(self):
        left = self.f.eval()       
        return self.tt.eval(left)
    
        
    def __repr__(self):
        return f'Term({self.f},{self.tt})'

class TermTail(Node):
    def __init__(self, op, f, tt):
        super(__class__,self)
        self.op = op
        self.f = f
        self.tt = tt
    
    def eval(self, left):
        eval_factor = self.f.eval()
        left = self.calc(left, eval_factor)
        return self.tt.eval(left)
    
        
    def __repr__(self):
        return f'TermTail({self.op},{self.f},{self.tt})'


class Factor(Node):
    def __init__(self, e, sign = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign

    def eval(self):
        if self.sign is '-':
            return -self.e.eval() if isinstance(self.e, Expr) else -float(self.e)
        else:
            return self.e.eval() if isinstance(self.e, Expr) else float(self.e)
    
    def __repr__(self):
        return f'Factor({self.sign},{self.e})'
    
    from collections.abc import Iterable
def isDigit(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class Scanner(object):
    def __init__(self, line):
        self.tokens = re.findall(r'[-+]|[0-9]*\.?[0-9]+|[*+-/()]', line) + ['EOL']
        
    def peak(self):
        return self.tokens[0]
    
    def shift(self):
        return self.tokens.pop(0)
        
    
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

class Parser(object):
    def __init__(self, scanner):
        self.tokens = scanner
        
    def parse(self):
        e = self.parseExpr()
        self.tokens.takeIt(['EOL'])
        return e
    
    def parseExpr(self):
        t = self.parseTerm()
        et = self.parseExprTail()
        return Expr(t  = t, et = et)
    
    def parseExprTail(self):
        if self.tokens.isType(['+', '-']):
            op = self.tokens.takeIt()
            t = self.parseTerm()
            et = self.parseExprTail()
            return ExprTail(op, t, et)
        return Empty()
        
    def parseTerm(self):
        f = self.parseFactor()
        tt = self.parseTermTail()
        return Term(f, tt)
    
    def parseTermTail(self):
        if self.tokens.isType(['*', '/']):
            op = self.tokens.takeIt()
            f = self.parseFactor()
            tt = self.parseTermTail()
            return TermTail(op, f, tt)
        return Empty()
        
    def parseFactor(self):
        if self.tokens.isType(['(']):
            self.tokens.takeIt('(')
            e = self.parseExpr()
            self.tokens.takeIt(')')
            return Factor(e)
        elif self.tokens.isType(['+', '-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            return Factor(f, sign=sign)
        else:
            number = self.tokens.takeIt(isDigit)
            return Factor(number)
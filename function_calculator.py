import re
import math

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
    
    def __str__(self):
        return ''

class Expr(Node):
    def __init__(self, t, et):
        super(__class__,self)
        self.t = t
        self.et = et
    
    def eval(self):
        return self.et.eval(self.t.eval())

    def __str__(self):
        return f'{str(self.t)}{str(self.et)}'
    
    def __repr__(self):
        return f'Expr({repr(self.t)}, {repr(self.et)})'
    
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

    def __str__(self):
        return f'{str(self.op)}{str(self.t)}{str(self.et)}'
    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.t)}, {repr(self.et)})'


class Term(Node):
    def __init__(self, f, expo, tt):
        super(__class__,self)
        self.f = f
        self.expo = expo
        self.tt = tt
    
    def eval(self):
        left = self.f.eval()
        left = -self.expo.eval(left) if left < 0 else self.expo.eval(left)
        return self.tt.eval(left)
    
    def __str__(self):
        return f'{str(self.f)}{str(self.expo)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.expo)},{repr(self.tt)})'

class TermTail(Node):
    def __init__(self, op, f, expo, tt):
        super(__class__,self)
        self.op = op
        self.f = f
        self.expo = expo
        self.tt = tt
    
    def eval(self, left):
        eval_factor = self.f.eval()
        left = self.calc(left, eval_factor)
        left = -self.expo.eval(left) if left < 0 else self.expo.eval(left)
        return self.tt.eval(left)
    
    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.exp)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.exp)},{repr(self.tt)})'


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
    
    def __str__(self):
        return f'({self.sign}{self.e})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)})'

class Variable(Node):
    def __init__(self, e):
        super(__class__,self)
        self.e = e
    
    def eval():
        pass
    
    def __str__(self):
        return str(self.e)
    def __repr__(self):
        return f'Variable({repr(self.e)})'

class AngleF(Node):
    def __init__(self, angleF, e):
        super(__class__,self)
        self.angleF = angleF
        self.e = e
    
    def __str__(self):
        return f'{str(self.angleF)}({str(self.e)})'
    def __repr__(self):
        return f'AngleF({repr(self.angleF)},{repr(self.e)})'

class Expo(Node):
    def __init__(self, f, expo):
        super(__class__,self)
        self. f = f
        self.expo = expo
    
    def eval(self, left):
        eval_factor = self.expo.eval(self.f.eval())
        return left**eval_factor
        
    
    def __str__(self):
        if isinstance(self.expo, Empty):
            return f'^({str(self.f)})' if isinstance(self.f, Expr) else f'^{str(self.f)}'
        else:
            return f'^({str(self.f)})^{str(self.expo)}' if isinstance(self.f, Expr) else f'^{str(self.f)}{str(self.expo)}'
    def __repr__(self):
        return f'Expo({repr(self.f)},{repr(self.expo)})'

class Log(Node):
    def __init__(self, logarithm, e):
        super(__class__,self)
        self.logarithm = logarithm
        self.e = e
    
    def eval(self, left):
        
    def __str__(self):
        return f'log{str(self.logarithm):.4}({str(self.e)})'
    def __repr__(self):
        return f'Log({repr(self.logarithm)},{repr(self.e)})'


from collections.abc import Iterable

class Scanner(object):
    def __init__(self, line):
        self.tokens = re.findall(r'[-+]|[a-z|A-Z]+|\.?[0-9]+|[*+-/()^]', line) + ['EOL']
        
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
        self.variables = {}
    
    def isDigit(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isAlpha(self, value):
        return value.isalpha()
    
    def parse(self):
        e = self.parseExpr()
        try:
            self.tokens.takeIt(['EOL'])    
            return e
        except:
            return 'Error'
    
    def parseExpr(self):
        print('Expr')
        t = self.parseTerm()
        et = self.parseExprTail()
        return Expr(t, et)
    
    def parseExprTail(self):
        print('ExprTail')
        if self.tokens.isType(['+', '-']):
            op = self.tokens.takeIt()
            print(op)
            t = self.parseTerm()
            et = self.parseExprTail()
            return ExprTail(op,t,et)
        print('Empty')
        return Empty()
    
    def parseTerm(self):
        print('Term')
        f = self.parseFactor()
        exp = self.parseExpo()
        tt = self.parseTermTail()
        return Term(f, exp, tt)
    
    def parseTermTail(self):
        print('TermTail')
        if self.tokens.isType(['*', '/']):
            op = self.tokens.takeIt()
            print(op)
            f = self.parseFactor()
            expo = self.parseExpo()
            tt = self.parseTermTail()
            return TermTail(op, f, expo, tt)
        print('Empty')
        return Empty()
    
    def parseFactor(self):
        print('Factor')
        if self.tokens.isType(['(']):
            print(self.tokens.takeIt())
            e = self.parseExpr()
            print(self.tokens.takeIt())
            return Factor(e)
        elif self.tokens.isType(['+','-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            return Factor(f, sign = sign)
        elif self.tokens.isType(isAlpha):
            var = self.parseVariable()
            return Factor(var)
        else:
            num = self.tokens.takeIt(self.isDigit)
            print(num)
            return Factor(num)
            
    def parseExpo(self):
        print('Expo')
        if self.tokens.isType(['^']):
            print(self.tokens.takeIt())
            f = self.parseFactor()
            expo = self.parseExpo()
            return Expo(f, expo)
        print('Empty')
        return Empty()
    
    def parseVariable(self):
        print('Variable')
        if self.tokens.isType(['sin','cos','tan']):
            angleF = self.parseAngleF()
            return Variable(angleF)
        elif self.tokens.isType(['log','ln']):
            log = self.parseLog()
            return Variable(log)
        else:
            alpha = self.tokens.takeIt(self.isAlpha)
            print(alpha)
            return Variable(alpha)
    
    def parseAngleF(self):
        print('angleF')
        #별로임
        angleF = self.tokens.takeIt()
        print(angleF)
        print(self.tokens.takeIt())
        e = self.parseExpr()
        print(self.tokens.takeIt())
        return AngleF(angleF, e)
    
    def parseLog(self):
        print('Log')
        log = self.tokens.takeIt()
        print(log)
        logarithm = E
        if self.tokens.isType(self.isDigit):
            logarithm = self.tokens.takeIt()
        print(self.tokens.takeIt())
        e = self.parseExpr()
        print(self.tokens.takeIt())            
        return Log(logarithm, e)
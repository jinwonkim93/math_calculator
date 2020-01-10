#log function
import math
import re

E = 2.718281828459045
PI = 3.141592653589793

greeks = ('alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta',
                    'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu',
                    'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon',
                    'phi', 'chi', 'psi', 'omega')

def logn(n, x = math.e):
    print(n/x)
    return 1 + logn(n/x, x) if n > (x-1) else 0

def lognNew(n, x = E):
    return math.log(n) / math.log(x)

def triangleFunction(func, expr):
    if func == 'sin':
        return math.sin(expr)
    elif func == 'cos':
        return math.cos(expr)
    elif func == 'tan':
        return math.tan(expr)


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

class Error(object):
    def __init__(self,error):
        self.error = error
    
    def __str__(self):
        return "Error"
    
    def __repr__(self):
        return "Error(Expr)"
    
    def eval(self):
        return self.error
        
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
    def __init__(self, f, tt):
        super(__class__,self)
        self.f = f
        self.tt = tt
    
    def eval(self):
        return self.tt.eval(self.f.eval())
    
    def __str__(self):
        return f'{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'Term({repr(self.f)},{repr(self.tt)})'

class TermTail(Node):
    def __init__(self, op, f,  tt):
        super(__class__,self)
        self.op = op
        self.f = f
        self.tt = tt
    
    def eval(self, left):
        eval_factor = self.f.eval()
        left = self.calc(left, eval_factor)
        return self.tt.eval(left)
    
    def __str__(self):
        return  f'{str(self.op)}{str(self.f)}{str(self.tt)}'
    def __repr__(self):
        return f'TermTail({repr(self.op)},{repr(self.f)},{repr(self.tt)})'


class Factor(Node):
    def __init__(self, e, sign = Empty(), expo = Empty()):
        super(__class__,self)
        self.e = e
        self.sign = sign
        self.expo = expo

    def eval(self):
        if self.sign is '-':
            return -self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else -self.expo.eval(float(self.e))
        else:
            return self.expo.eval(self.e.eval()) if isinstance(self.e, (Expr, Variable, Factor)) else self.expo.eval(float(self.e))
    
    def __str__(self):
        return f'({self.sign}{self.e}{self.expo})' if isinstance(self.e, Expr) else f'{self.sign}{self.e}{self.expo}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.e)},{repr(self.expo)})'

class Variable(Node):
    def __init__(self, e):
        super(__class__,self)
        self.e = e
    
    def eval(self):
        return self.e.eval() if isinstance(self.e, (Expr, Log, AngleF, Symbol)) else float(self.e)
    
    def __str__(self):
        return str(self.e)
    def __repr__(self):
        return f'Variable({repr(self.e)})'

class AngleF(Node):
    def __init__(self, angleF, e):
        super(__class__,self)
        self.angleF = angleF
        self.e = e
    def eval(self):
        return triangleFunction(self.angleF, self.e.eval())
    
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
    
    def eval(self):
        return lognNew(self.e.eval(),self.logarithm)
        
    def __str__(self):
        return f'log{str(self.logarithm):.4}({str(self.e)})'
    def __repr__(self):
        return f'Log({repr(self.logarithm)},{repr(self.e)})'

class Symbol(object):
    def __init__(self, symbol,subExpr = None):
        self.symbol = symbol
        self.value = None
        self.subExpr = subExpr
        
    def insert(self, value, subExpr = None):
        self.value = value
        self.subExpr = subExpr
    
    def eval(self):
        return self.value.eval() if isinstance(self.value, Expr) else float(self.value)
    
    def __repr__(self):
        return f'({repr(self.subExpr)}' if self.subExpr is not None else f'({repr(self.value)})'
    def __str__(self):
        return f'({self.subExpr})' if self.subExpr is not None else f'({self.value})'

from collections.abc import Iterable
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

class Parser(object):
    def __init__(self, scanner):
        self.tokens = scanner
        self.variables = {}
    

    
    def insertValue(self):
        for name, symbol in self.variables.items():
            value = input(f'what is value of {name}: ')
            if self.tokens.isDigit(value):
                symbol.insert(value)
            else:
                tok = Scanner(value)
                sub_parser = Parser(tok)
                sub_expr = sub_parser.parse()
                sub_parser.insertValue()
                symbol.insert(sub_expr.eval(), subExpr = sub_expr)
                
            
    def parse(self):
        try:
            e = self.parseExpr()
            self.tokens.takeIt(['EOL'])    
            return e
        except Exception as e:
            return Error(e)
    
    def parseExpr(self):
        t = self.parseTerm()
        et = self.parseExprTail()
        return Expr(t, et)
    
    def parseExprTail(self):
        if self.tokens.isType(['+', '-']):
            op = self.tokens.takeIt()
            t = self.parseTerm()
            et = self.parseExprTail()
            return ExprTail(op,t,et)
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
            self.tokens.takeIt()
            e = self.parseExpr()
            self.tokens.takeIt()
            expo = self.parseExpo()
            return Factor(e, expo = expo)
        elif self.tokens.isType(['+','-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseExpo()
            return Factor(f, sign = sign, expo = expo)
        elif self.tokens.isType(self.tokens.isAlpha):
            var = self.parseVariable()
            expo = self.parseExpo()
            return Factor(var, expo = expo)
        elif self.tokens.isType(self.tokens.isDigit):
            num = self.tokens.isSpecialNum(self.tokens.takeIt())
            expo = self.parseExpo()
            return Factor(num, expo = expo)
        else:
            raise Exception("Invalid Factor")
            
    def parseExpo(self):
        if self.tokens.isType(['^']):
            self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseExpo()
            return Expo(f, expo)
        return Empty()
    
    def parseVariable(self):
        if self.tokens.isType(['sin','cos','tan']):
            angleF = self.parseAngleF()
            return Variable(angleF)
        elif self.tokens.isType(['log','ln']):
            log = self.parseLog()
            return Variable(log)
        else:
            alpha = self.tokens.takeIt(self.tokens.isAlpha)
            if alpha == 'EOL': raise Exception("Invalid Variable")
            elif alpha in self.variables.keys():
                alpha = self.variables.get(alpha)
                return Variable(alpha)
            else:
                sym = Symbol(alpha)
                self.variables[alpha] = sym
                return Variable(sym)
    
    def parseAngleF(self):
        angleF = self.tokens.takeIt()
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()
        return AngleF(angleF, e)
    
    def parseLog(self):
        log = self.tokens.takeIt()
        logarithm = E
        if self.tokens.isType(self.tokens.isDigit):
            logarithm = self.tokens.takeIt()
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()         
        return Log(logarithm, e)
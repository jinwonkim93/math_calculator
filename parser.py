from expression import Expr, ExprTail
from term import Term, TermTail
from factor import Factor, Variable
from math_function import Log, Exponential, Symbol, AngleFunction
from error import Error
from empty import Empty
from mathematical_constant import *



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
            expo = self.parseExponential()
            return Factor(e, expo = expo)
        elif self.tokens.isType(['+','-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseExponential()
            return Factor(f, sign = sign, expo = expo)
        elif self.tokens.isType(self.tokens.isAlpha):
            var = self.parseVariable()
            expo = self.parseExponential()
            return Factor(var, expo = expo)
        elif self.tokens.isType(self.tokens.isDigit):
            num = self.tokens.isSpecialNum(self.tokens.takeIt())
            expo = self.parseExponential()
            return Factor(num, expo = expo)
        else:
            raise Exception("Invalid Factor")
            
    def parseExponential(self):
        if self.tokens.isType(['^']):
            self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseExponential()
            return Exponential(f, expo)
        return Empty()
    
    def parseVariable(self):
        if self.tokens.isType(['sin','cos','tan']):
            angleF = self.parseAngleFunction()
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
    
    def parseAngleFunction(self):
        angleF = self.tokens.takeIt()
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()
        return AngleFunction(angleF, e)
    
    def parseLog(self):
        log = self.tokens.takeIt()
        logarithm = E
        if self.tokens.isType(self.tokens.isDigit):
            logarithm = self.tokens.takeIt()
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()         
        return Log(logarithm, e)
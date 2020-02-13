from expression import Expr
from expression_tail import ExprTail
from term import Term
from term_tail import TermTail
from factor import Factor, Variable, Constant, Symbol, Log,  Sin, Cos, Tan, Sec, Csc, Cot, ConstantE, Pi, Parenthesis
from factor_tail import FactorTail
from error import Error, NonDerivableError
from empty import Empty
from mathematical_constant import *
from calculator import  clearExpr
from utils import sortVariable, list2str



class Parser(object):
    def __init__(self, scanner):
        self.tokens = scanner
        self.variables = {}
        self.domain = {}
    
    def insertValue2(self, value, name):
        if self.tokens.isDigit(value):
            self.variables[name].insert(value)
    
    def insertValue(self, value):
        for name, symbol in self.variables.items():
            if self.tokens.isDigit(value[name]):
                symbol.insert(value[name])
            else:
                tok = Scanner(value)
                sub_parser = Parser(tok)
                sub_expr = sub_parser.parse()
                sub_parser.insertValue()
                symbol.insert(sub_expr.canonicalize())
    
    def getInvalidDomain(self,v,invalid):
        if isinstance(v, (Variable,str)):
            if len(self.domain) == 0: 
                self.domain[v] = invalid
                return True
            else:
                for key in self.domain.keys():
                    if not key == v:
                        self.domain[v] = invalid
                        return True
        
        elif isinstance(v,list):
            d = ''
            for e in v:
                d +=str(e)
            if len(self.domain) == 0: 
                self.domain[d] = invalid
                return True
            else:
                for key in self.domain.keys():
                    if not key == d:
                        self.domain[d] = invalid
                        return True

        return False
    
    def getDomain(self):
        res = []
        for key in self.domain:
            res.append([key,self.domain[key]])
        return res
    def getVariables(self):
        return self.variables
    
    def parse(self):
        try:
            e = self.parseExpr()
            self.tokens.takeIt(['EOL'])    
            return e
        except Exception as e:
            return Error(e)
        # e = self.parseExpr()
        # self.tokens.takeIt(['EOL'])    
        # return e
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
            # if op == '/': 
            v = f.canonicalize()
            self.getInvalidDomain(v,'!= 0')
            tt = self.parseTermTail()
            return TermTail(op, f, tt)
        return Empty()
    
    def parseFactor(self):
        if self.tokens.isType(['(']):
            self.tokens.takeIt()
            e = self.parseExpr()
            self.tokens.takeIt()
            expo = self.parseFactorTail()
            return Factor(e, expo = expo)
        elif self.tokens.isType(['+','-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseFactorTail()
            return Factor(f, sign = sign, expo = expo)
        elif self.tokens.isType(self.tokens.isAlpha):
            var = self.parseVariable()
            expo = self.parseFactorTail()
            return Factor(var, expo = expo)
        elif self.tokens.isType(self.tokens.isDigit):
            num = Constant(self.tokens.takeIt())
            expo = self.parseFactorTail()
            return Factor(num, expo = expo)
        else:
            raise Exception("Invalid Factor")
            
    def parseFactorTail(self):
        if self.tokens.isType(['^']):
            self.tokens.takeIt()
            f = self.parseFactor()
            f_eval = f.eval()
            if abs(f_eval) > 0 and abs(f_eval) < 1:
                
                self.getInvalidDomain('x','> 0')
            expo = self.parseFactorTail()
            return FactorTail(f, expo)
        return Empty()
    
    def parseVariable(self):
        if self.tokens.isType(trigonometric_functions):
            angleF = self.parseAngleFunction()
            return Variable(angleF)
        elif self.tokens.isType(['log','ln']):
            log = self.parseLog()
            v = log.e.canonicalize()
            self.getInvalidDomain(v,'> 0')
            return Variable(log)
        elif self.tokens.isType(self.tokens.isSpecialNum):
            specialNum = self.parseSpecialNum()
            return Variable(specialNum)
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
        if angleF == 'sin':
            return Sin(e)
        elif angleF == 'cos':
            return Cos(e)
        elif angleF == 'tan':
            tan = Tan(e)
            v = tan.e.canonicalize()
            self.getInvalidDomain(v,' != n*pi + pi/2 (n is real_number)')
            return tan
        elif angleF == 'csc':
            csc = Csc(e)
            v = csc.e.canonicalize()
            self.getInvalidDomain(v,' != n*pi (n is real_number)')
            return csc
        elif angleF == 'sec':
            sec = Sec(e)
            v = sec.e.canonicalize()
            self.getInvalidDomain(v,' != n*pi + pi/2(n is real_number)')
            return sec
        elif angleF == 'cot':
            cot = Cot(e)
            v = cot.e.canonicalize()
            self.getInvalidDomain(v,' != n*pi (n is real_number)')
            return cot
         
    
    def parseLog(self):
        log = self.tokens.takeIt()
        logarithm = E
        if self.tokens.isType(self.tokens.isDigit):
            logarithm = self.tokens.takeIt()
        elif self.tokens.isType(['-']):
            raise Exception("invalid_log_term")
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()         
        return Log(logarithm, e)

    def parseSpecialNum(self):
        num = self.tokens.takeIt()
        if num == 'e':
            return ConstantE()
        elif num == 'pi':
            return Pi()
        raise NotImplementedError
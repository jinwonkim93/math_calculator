from expression import Expr
from expression_tail import ExprTail
from term import Term
from term_tail import TermTail
from factor_new import Factor, Variable, Constant, Symbol
from math_function import Log,  Sin, Cos, Tan, Sec, Csc, Cot
from factor_tail import FactorTail
from error import Error
from empty import Empty
from mathematical_constant import *



class Parser(object):
    def __init__(self, scanner):
        self.tokens = scanner
        self.variables = {}
        self.domain = {}
    
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
                symbol.insert(sub_expr.eval())
    
    def getInvalidDomain(self,v,invalid):
        if isinstance(v, Variable):
            if len(self.domain) == 0: 
                self.domain[v] = invalid
                return True
            else:
                for key in self.domain.keys():
                    if not key == v.e:
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
        
    def getDerivative(self, semi_expression):
        if self.variables:
            semi_expression = semi_expression.eval()
            derivatives = []
            for name, symbol in self.variables.items():
                try:
                    temp = []
                    if isinstance(semi_expression, list):
                        for value in semi_expression:
                            if isinstance(value, (int,float)):
                                if len(temp) > 0: temp.pop()

                            elif value in ('+', '-', '*', '/'):
                                temp.append(value)                            
                            else:
                                derivation = value.getDerivative(symbol)
                                if isinstance(derivation, Variable):
                                    if derivation.coeff == 0:
                                        if len(temp) >0:temp.pop()
                                    else:
                                        if len(temp) == 1: temp.pop()
                                        temp.append(derivation)
                                
                                elif derivation == 0:
                                    if len(temp) > 0: temp.pop()
                                else:
                                    if len(temp) == 1: temp.pop()
                                    temp.append(derivation)

                        d = ''
                        for element in temp:
                            d += str(element)
                        print(f'd({semi_expression})/d{name} = ', d)
                        derivatives.append((name,d))
                    else:
                        if isinstance(semi_expression, (int,float)):
                            return NotImplemented
                        else:
                            print(f'd({semi_expression})/d{name} = ', semi_expression.getDerivative(symbol))
                            derivatives.append((name,semi_expression.getDerivative(symbol)))
                except:
                    return semi_expression
            return derivatives

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
            if op == '/': 
                v = f.eval()
                print('vvvv',v, type(v))
                self.getInvalidDomain(v,'!=0')
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
            num = Constant(self.tokens.isSpecialNum(self.tokens.takeIt()))
            expo = self.parseFactorTail()
            return Factor(num, expo = expo)
        else:
            raise Exception("Invalid Factor")
            
    def parseFactorTail(self):
        if self.tokens.isType(['^']):
            self.tokens.takeIt()
            f = self.parseFactor()
            expo = self.parseFactorTail()
            return FactorTail(f, expo)
        return Empty()
    
    def parseVariable(self):
        if self.tokens.isType(trigonometric_functions):
            angleF = self.parseAngleFunction()
            return Variable(angleF)
        elif self.tokens.isType(['log','ln']):
            log = self.parseLog()
            v = log.e.eval()
            self.getInvalidDomain(v,'> 0')
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
        if angleF == 'sin':
            return Sin(e)
        elif angleF == 'cos':
            return Cos(e)
        elif angleF == 'tan':
            tan = Tan(e)
            v = tan.e.eval()
            self.getInvalidDomain(v,'n*pi + pi/2 (n is real_number)')
            return tan
        elif angleF == 'csc':
            csc = Csc(e)
            v = csc.e.eval()
            self.getInvalidDomain(v,'n*pi (n is real_number)')
            return csc
        elif angleF == 'sec':
            sec = Sec(e)
            v = sec.e.eval()
            self.getInvalidDomain(v,'n*pi + pi/2(n is real_number)')
            return sec
        elif angleF == 'cot':
            cot = Cot(e)
            v = cot.e.eval()
            self.getInvalidDomain(v,'n*pi (n is real_number)')
            return cot
         
    
    def parseLog(self):
        log = self.tokens.takeIt()
        logarithm = E
        if self.tokens.isType(self.tokens.isDigit):
            logarithm = self.tokens.takeIt()
        self.tokens.takeIt()
        e = self.parseExpr()
        self.tokens.takeIt()         
        return Log(logarithm, e)
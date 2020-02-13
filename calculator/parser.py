from calculator.core2 import Error, Empty, Expression, ExpressionTail, Term, TermTail, Factor, FactorTail, Variable, Sin, Cos, Log, ConstantE, Pi
from calculator.mathematical_constant import *

class Parser(object):
    def __init__(self, scanner):
        self.tokens = scanner
        self.variables = {}
        self.domain = {}

    def insertValue(self, value):
        for name, symbol in self.variables.items():
            if self.tokens.isDigit(value[name]):
                symbol.insert(value[name])
        return True
    def getVariables(self):
        return self.variables
    def parse(self):
        try:
            e = self.parseExpr()
            self.tokens.takeIt(['EOL'])    
            return e
        except Exception as e:
            raise e
            # return Error(e)

    def parseExpr(self):
        t = self.parseTerm()
        et = self.parseExprTail()
        return Expression(t, et)
    
    def parseExprTail(self):
        if self.tokens.isType(['+', '-']):
            op = self.tokens.takeIt()
            t = self.parseTerm()
            et = self.parseExprTail()
            return ExpressionTail(t,op,et)
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
        if self.tokens.isType(['+', '-']):
            sign = self.tokens.takeIt()
            f = self.parseFactor()
            return Factor(v = f,sign=sign)
        else:
            v = self.parseValue()
            ft = self.parseFactorTail()
            return Factor(v=v, ft =ft)

    def parseValue(self):
        if self.tokens.isType(['(']):
            self.tokens.takeIt()
            e = self.parseExpr()
            self.tokens.takeIt()
            # return Value(e)
            return e
        elif self.tokens.isType(self.tokens.isFunction):
            function = self.parseFunction()
            return function
        elif self.tokens.isType(self.tokens.isSpecialNum):
            specialNum = self.parseSpecialNum()
            # return Value(specialNum)     
            return specialNum     
        elif self.tokens.isType(self.tokens.isAlpha):
            var = self.parseVariable()
            # return Value(var)
            return var
        elif self.tokens.isType(self.tokens.isDigit):
            num = self.tokens.takeIt()
            # return Value(float(num))
            return float(num)
            
    def parseFactorTail(self):
        if self.tokens.isType(['^']):
            self.tokens.takeIt()
            f = self.parseFactor()
            # f = self.parseVariable()
            # factorTail = self.parseFactorTail()
            # return FactorTail(f, factorTail)
            return FactorTail(f)
        return FactorTail(Factor(1.0))
    
    def parseVariable(self):
        alpha = self.tokens.takeIt(self.tokens.isAlpha)
        if alpha == 'EOL': raise Exception("Invalid Variable")
        elif alpha in self.variables.keys():
            alpha = self.variables.get(alpha)
            return alpha
        else:
            variable = Variable(alpha)
            self.variables[alpha] = variable
            return variable

    def parseFunction(self):
        if self.tokens.isType(trigonometric_functions):
            angleF = self.parseAngleFunction()
            return angleF
        elif self.tokens.isType(['log','ln']):
            log = self.parseLog()
            return log
        elif self.tokens.isType(self.tokens.isSpecialNum):
            specialNum = self.parseSpecialNum()
            return specialNum

    
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
            return tan
        elif angleF == 'csc':
            csc = Csc(e)
            return csc
        elif angleF == 'sec':
            sec = Sec(e)
            return sec
        elif angleF == 'cot':
            cot = Cot(e)
            return cot
    
    def parseLog(self):
        log = self.tokens.takeIt()
        base = E

        self.tokens.takeIt()
        value = self.parseExpr()
        if self.tokens.isType(','):
            self.tokens.takeIt()
            base = value
            value = self.parseExpr()
        self.tokens.takeIt()
        return Log(base, value)

    def parseSpecialNum(self):
        num = self.tokens.takeIt()
        if num == 'e':
            return ConstantE()
        elif num == 'pi':
            return Pi()
        raise NotImplementedError
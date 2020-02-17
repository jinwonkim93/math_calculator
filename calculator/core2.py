import math
from copy import deepcopy, copy

def checkParenthesisValid(term):
    coeff = term.coefficient
    factor = term.getFactor()
    factorTail = factor.factorTail
    expr = factor.getValue()
    return coeff == 1 and factorTail.factor.sign != '-' and factorTail.factor.v == 1 and len(term) == 1


class Error(object):
    def __init__(self, error):
        self.error = error
    
    def __str__(self):
        return "Error"

    def __repr__(self):
        return "Error(Expr)"
        

class Empty(object):
    def __init__(self):
        self.value = 'Empty'

    def eval(self,left,values):
        return left

    def canonicalize(self,left):
        return left

    def getDerivative(self,symbol):
        return self

    def getTermDerivative(self,symbol,term):
        #term 말고 termtail만 돌고 나중에 마지막이랑 합치면 되지
        return term

    def add(self,left):
        return left

    def compareEquality(self,other):
        if self.__class__ == other.__class__: return 0
        return -1

    def getVariables(self, variables):
        return variables

    def insertTail(self, tail):
        return tail

    def getNew(self):
        return self

    def __neg__(self):
        return self

    def __len__(self):
        return 0

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Empty'
        

class Expression(object):
    def __init__(self,t, et=Empty()):
        self.term = t
        self.expressionTail = et

    def eval(self, values):
        return self.expressionTail.eval(self.term.eval(values), values)

    def canonicalize(self):
        term = self.term.canonicalize()
        expressionTail = self.expressionTail.getNew()
        #term이 expression일때 최종 expression에 확장
        if isinstance(term.getFactor().getValue(),Expression) and checkParenthesisValid(term):
            temp_expr = term.getFactor().getValue()
            if term.coefficient < 0:
                temp_expr = -temp_expr
            term = temp_expr.getTerm()
            temp_et = temp_expr.getNextExpr()
            if not isinstance(temp_et, Empty):
                et = temp_et
                et.insertTail(expressionTail)
            else: et = expressionTail
            return et.canonicalize(Expression(term))
        return expressionTail.canonicalize(Expression(term))

    def getDerivative(self,symbol):
        left = self.term.getDerivative(symbol)
        et = self.expressionTail.getDerivative(symbol)
        # print(left, et)
        return Expression(left,et).dropZero()

    def isDifferentiable(self,symbol):
        if self.term.isDifferentiable(symbol):
            if isinstance(self.expressionTail,Empty): return True
            elif self.expressionTail.isDifferentiable(symbol):
                return True
        return False

    def mulTerm(self,term):
        #term 또는 expr n번 반복
        right_term = term
        right_nextExpr = Empty()
        if isinstance(term.getFactor().getValue(), Expression)  and checkParenthesisValid(term):
            right_expr = term.getFactor().getValue()
            right_term = right_expr.getTerm()
            right_nextExpr = right_expr.getNextExpr()
        result = Expression(Empty())
        while not isinstance(right_term, Empty):
            left_term = self.getTerm()
            left_nextExpr = self.getNextExpr()
            while not isinstance(left_term, Empty):
                res = left_term.mul(right_term)
                result.insertTerm(res)
                left_term = left_nextExpr.getTerm() if isinstance(left_nextExpr, ExpressionTail) else Empty()
                left_nextExpr = left_nextExpr.getNextExpr() if isinstance(left_nextExpr, ExpressionTail) else Empty()
            right_term = right_nextExpr.getTerm() if isinstance(right_nextExpr, ExpressionTail) else Empty()
            right_nextExpr = right_nextExpr.getNextExpr() if isinstance(right_nextExpr, ExpressionTail) else Empty()
        return result

    def addTerm(self,term):
        if isinstance(term,Term):
            et = ExpressionTail(term)
        elif isinstance(term, Expression):
            et = ExpressionTail(t=term.term,et=term.expressionTail)
        result = et.calc(self,term)
        return result

    def getTerm(self):
        return self.term

    def getNextExpr(self):
        return self.expressionTail

    def insertTerm(self, term):
        term = term.getNew()
        if isinstance(self.term, Empty):
            self.term = term
        elif isinstance(self.expressionTail, Empty):
            self.expressionTail = ExpressionTail(t=term)
        else:
            self.expressionTail.insertTail(ExpressionTail(t=term))

    def insertExprTail(self, et):
        et = et.getNew()
        if isinstance(self.expressionTail, Empty):
            self.expressionTail = et
        else:
            self.expressionTail.insertTail(et)

    def dropZero(self):
        term = self.getTerm()
        nextExpr = self.getNextExpr()
        result = Expression(Empty())
        allZero = True
        while not isinstance(term, Empty):
            if term.coefficient != 0:
                result.insertTerm(term)
                allZero = False
            term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
            nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        if allZero: result = Expression(Term(Constant(),coeff = 0))
        return result

    def getVariables(self, variables=None):
        if variables == None: variables = set([])
        return self.expressionTail.getVariables(self.term.getVariables(variables))

    def getNew(self):
        term = self.term.getNew()
        et = self.expressionTail.getNew()
        return Expression(term,et)

    def __len__(self):
        result = 1
        result += len(self.expressionTail)
        return result

    def __eq__(self, expression):
        if self.__class__ != expression.__class__:return False
        return str(self) == str(expression)

    def __neg__(self):
        self.term = -self.term
        self.expressionTail = -self.expressionTail
        return self

    def __str__(self):
        return f'{str(self.term)}{str(self.expressionTail)}'
        
    def __repr__(self):
        return f'Expr({repr(self.term)}, {repr(self.expressionTail)})'


class ExpressionTail(object):
    def __init__(self, t, op='+', et=Empty()):
        self.op = op
        self.term = t
        self.expressionTail = et

    def eval(self, left, values):
        right = self.term.eval(values)
        left = left+right
        return self.expressionTail.eval(left, values)

    def canonicalize(self, left):
        s = self.getNew()
        if s.op == '-': s.term, s.op = -s.term, '+'
        s.term = s.term.canonicalize()
        if isinstance(s.term.getFactor().getValue(), Expression) and checkParenthesisValid(s.term):
            temp_expr = s.term.getFactor().getValue()
            if s.term.coefficient < 0: temp_expr = -temp_expr
            s.term = temp_expr.getTerm()
            s.insertTail(temp_expr.getNextExpr())
        return s.expressionTail.canonicalize(s.calc(left,s.term))

    def getDerivative(self, symbol):
        right = self.term.getDerivative(symbol)
        et = self.expressionTail.getDerivative(symbol)
        return ExpressionTail(t=right,et=et) 

    def isDifferentiable(self, symbol):
        if self.term.isDifferentiable(symbol):
            if isinstance(self.expressionTail,Empty): return True
            elif self.expressionTail.isDifferentiable(symbol):
                return True
        return False

    #더하기, 빼기, insert하기
    def calc(self, expr, term):
        left_term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        result = Expression(Empty())
        noSameTerm = True
        while not isinstance(left_term, Empty):
            compare = left_term.compareTermPrecedence(term)
            if compare == 0:
                left_term.add(term)
                result.insertTerm(left_term)
                result.insertExprTail(nextExpr)
                noSameTerm = False
                break  
            elif compare == 1:
                result.insertTerm(term)
                result.insertTerm(left_term)
                result.insertExprTail(nextExpr)
                noSameTerm = False
                break
            else:
                result.insertTerm(left_term)
                left_term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
                nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        if noSameTerm: result.insertTerm(term)
        result = result.dropZero()
        return result

    def getTerm(self):
        return self.term

    def getNextExpr(self):
        return self.expressionTail

    def insertTail(self,expressionTail):
        if isinstance(self.expressionTail, Empty):
            self.expressionTail = expressionTail
        else:
            self.expressionTail.insertTail(expressionTail)

    def getVariables(self, variables):
        return self.expressionTail.getVariables(self.term.getVariables(variables))

    def getNew(self):
        term = self.term.getNew()
        et = self.expressionTail.getNew()
        return ExpressionTail(t=term,et=et,op=self.op)

    def __neg__(self):
        self.term = -self.term
        self.expressionTail = -self.expressionTail
        return self

    def __len__(self):
        result = 1
        result += len(self.expressionTail)
        return result

    def __str__(self):
        return f'{str(self.op)}{str(self.term)}{str(self.expressionTail)}'

    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.term)}, {repr(self.expressionTail)})'


class Term(object):
    def __init__(self, f,tt = Empty(),coeff = 1.0):
        self.coefficient = coeff
        self.factor = f
        self.termTail = tt

    def eval(self, values):
        result = self.coefficient * self.factor.eval(values)
        return self.termTail.eval(result, values)

    def canonicalize(self):
        #empty이면 term이 리턴되어야 하기 때문에 term을 감싸야함
        factor = self.factor.canonicalize()
        coeff = self.coefficient
        if factor.sign == '-': coeff, factor.sign = -coeff, Empty()
        if isinstance(factor.getValue(), float):
            coeff *= factor.getValue()
            factor = Constant(ft=factor.factorTail)
        return self.termTail.canonicalize(Term(f=factor,coeff=coeff))

    def getDerivative(self,symbol):
        if self.isDifferentiable(symbol):
            # 계수 * 지수, 지수-1, 나머지 상수처리
            expo, factor = self.factor.getDerivative(symbol)
            if isinstance(factor, Empty): return Term(factor,coeff=0)
            coeff = self.coefficient * expo
            term = Term(f=factor,coeff=coeff)
            tt = self.termTail.getTermDerivative(symbol, term)
            return tt
        else:
            return Term(Constant(), coeff = 0)

    def isDifferentiable(self,symbol):
        left = self
        for idx in range(len(self)):
            left_f = left.getFactor()
            if left_f.isDifferentiable(symbol): return True
            left = left.getNextTerm()
        return False

    def add(self, term):
        self.coefficient = self.coefficient+term.coefficient
        if self.coefficient == 0: self.factor = Constant()

    def mul(self, term):
        coeff = self.coefficient * term.coefficient
        left_term = Term(self.factor, self.termTail, coeff)
        termTail = TermTail(f=term.getFactor())
        result = termTail.calc(left_term,termTail.factor)
        return result

    def getFactor(self):
        return self.factor

    def getNextTerm(self):
        return self.termTail

    def compareEquality(self, term):
        left = self
        right = term
        if len(self) == len(term):
            for idx in range(len(self)):
                left_f = left.getFactor()
                right_f = right.getFactor()
                if not left_f.compareEquality(right_f): return False
                left = left.getNextTerm()
                right = right.getNextTerm()
            return True
        return False

    def insertFactor(self,factor):
        factor = factor.getNew()
        if isinstance(self.factor, Empty): self.factor = factor
        elif isinstance(self.factor, Constant): self.factor = factor
        elif isinstance(self.termTail, Empty): self.termTail = TermTail(f=factor)
        else: self.termTail.insertTail(TermTail(f=factor))

    def insertTail(self,tt):
        tt = tt.getNew()
        if isinstance(self.termTail, Empty):
            self.termTail = tt
        else:
            self.termTail.insertTail(tt)

    def compareTermPrecedence(self, term):
        if self.compareEquality(term): return 0
        elif isinstance(self.factor, Constant): return -1
        elif isinstance(term.factor,Constant): return 1
        left = str(self)
        right = str(term)
        return 1 if left > right else -1

    def pow(self,power_factor):
        coeff = self.coefficient**power_factor
        factor = self.getFactor()
        factor = factor.pow(power_factor)

    def getVariables(self, variables):
        return self.termTail.getVariables(self.factor.getVariables(variables))

    def getNew(self):
        factor = self.factor.getNew()
        tt = self.termTail.getNew()
        coeff = self.coefficient
        return Term(factor,tt, coeff=coeff)

    def __eq__(self,term):
        if self.factor == term.factor:
            if self.termTail == term.termTail:
                return True
        return False

    def __neg__(self):
        self.coefficient = -self.coefficient
        return self

    def __len__(self):
        result = 1
        result += len(self.termTail)
        return result

    def __str__(self):
        if isinstance(self.factor,Constant):
            return f'{self.coefficient}{str(self.factor)}{str(self.termTail)}'
        return f'{self.coefficient}*{str(self.factor)}{str(self.termTail)}' if self.coefficient != 1 else f'{str(self.factor)}{str(self.termTail)}'

    def __repr__(self):
        return f'Term({self.coefficient},{repr(self.factor)},{repr(self.termTail)})'


class TermTail(object):
    def __init__(self, op ='*', f = Empty(), tt = Empty()):
        self.op = op
        self.factor = f
        self.termTail = tt

    def eval(self, left, values):
        right = self.factor.eval(values)
        left = left*right
        return self.termTail.eval(left, values)
        
    def canonicalize(self, left):
        s = self.getNew()
        if s.op == '/':
            s.factor.makeFactorTailNeg()
            s.op = '*'
        right = s.factor.canonicalize()
        return s.termTail.canonicalize(s.calc(left, right))

    def getTermDerivative(self, symbol, term):
        expo, factor = self.factor.getDerivative(symbol)
        term.coefficient = term.coefficient * expo
        # 만약에 1이거나 
        term.insertFactor(factor)
        # term = term.insertFactor(factor)
        tt = self.termTail.getTermDerivative(symbol,term)
        return tt

    def calc(self, factors,factor):
        coeff = factors.coefficient
        result = Term(Empty(), coeff = coeff)
        if isinstance(factor.getValue(),float):
            #coeff에 연산
            coeff = coeff*factor.getValue()
            factors.coefficient = coeff
            factor = Constant()
            if coeff == 0: return Term(Constant(),coeff=0)
            return factors

        left_factor = factors.getFactor()
        nextFactor = factors.getNextTerm()
        noSameFactor = True
        while not isinstance(left_factor, Empty):
            compare = left_factor.compareFactorMultiplyPrecedence(factor)
            if compare == 0:
                left_factor = left_factor.mul(factor)
                result.insertFactor(left_factor)
                result.insertTail(nextFactor)
                noSameFactor = False
                break
            elif compare == 1:
                result.insertFactor(factor)
                result.insertFactor(left_factor)
                result.insertTail(nextFactor)
                noSameFactor = False
                break
            else:
                result.insertFactor(left_factor)
                left_factor = nextFactor.getFactor() if isinstance(nextFactor, TermTail) else Empty()
                nextFactor = nextFactor.getNextTerm() if isinstance(nextFactor, TermTail) else Empty()
        if noSameFactor: result.insertFactor(factor)
        return result

    def getFactor(self):
        return self.factor

    def getNextTerm(self):
        return self.termTail

    def insertTail(self,termTail):
        if isinstance(self.termTail,Empty):
            self.termTail = termTail
        else:
            self.termTail.insert(termTail)

    def getVariables(self, variables):
        return self.termTail.getVariables(self.factor.getVariables(variables))

    def getNew(self):
        factor = self.factor.getNew()
        tt = self.termTail.getNew()
        return TermTail(f=factor,tt=tt,op=self.op)

    def __eq__(self, termTail):
        if isinstance(termTail, Empty): return False
        if self.factor == termTail.factor:
            if self.termTail == termTail.termTail:
                return True
        return False

    def __len__(self):
        result = 1
        result += len(self.termTail)
        return result

    def __str__(self):
        return f'{self.op}{str(self.factor)}{str(self.termTail)}'

    def __repr__(self):
        return f'TermTail({self.op},{repr(self.factor)},{repr(self.termTail)})'


class Factor(object):
    def __init__(self, v, sign = Empty(), ft = Empty()):
        self.sign = sign
        self.v = v
        self.factorTail = ft

    def eval(self, values):
        v = self.v if isinstance(self.v, float) else self.v.eval(values)
        return self.factorTail.eval(v, values)

    def canonicalize(self):
        #factor은 factor을 리턴해야함
        v = self.v.canonicalize() if not isinstance(self.v,float) else self.v
        if not isinstance(v, Factor): v = Factor(v)
        v = self.factorTail.canonicalize(v)
        if self.sign == '-': v = -v
        return v

    def getDerivative(self, symbol):
        if self.v.isDifferentiable(symbol):
            print(type(self.factorTail))
            expo, factorTail = self.factorTail.getDerivative(symbol) if isinstance(self.factorTail, FactorTail) else 1, Empty()
            if factorTail.getValue() == 0:
                return expo, Constant()
            return expo, Factor(self.v, factorTail)
        return 1, self

    def isDifferentiable(self, symbol):
        return self.v.isDifferentiable(symbol)

    def add(self,factor):
        right = factor.v
        if self.sign == '-':
            self.v = -self.v
        if factor.sign == '-':
            right = -right
        self.v = self.v+right
        if abs(self.v) < 0: self.sign = '-'
        else: self.sign = Empty()

    def mul(self,factor):
        if isinstance(self,Constant): return factor
        factorTail = self.factorTail.add(factor.factorTail)
        if factorTail.factor.getValue() == 0: return Constant()
        return Factor(v=self.v,ft=factorTail)
        # return Factor(result,result_sign, self.factorTail)

    def compareFactorPrecedence(self,factor):
        compare = self.compareEquality(factor)
        if compare == 0: return 0
        left = str(self.getValue())
        right = str(factor.getValue())
        if left == right:
            compare = self.factorTail.comparePriority(factor.factorTail)
            if compare: return -1
            else:return 1
        elif left > right: return 1
        else:return -1

    def compareFactorMultiplyPrecedence(self,factor):
        if self.compareEquality(factor): return 0
        left = str(self)
        right = str(factor)
        if left > right: return 1
        else:return -1

    def getPriority(self):
        result = 0
        if isinstance(self.v, Variable):
            result += 1
        if isinstance(self.factorTail, FactorTail):
            result += self.factorTail.getPriority()
        return result

    def compareEquality(self,factor):
        if self == factor: return True
        return False

    def makeFactorTailNeg(self):
        if isinstance(self.factorTail,Empty):
            self.factorTail = FactorTail(f=Factor(1.0),ft=Empty())
        self.factorTail = -self.factorTail

    def getSign(self):
        return self.sign

    def pow(self,factor):
        if factor.sign == '-':
            factor.v = -factor.v
        return self.v**factor.v

    def getValue(self):
        return self.v

    def getVariables(self,variables):
        return self.v.getVariables(variables) if not isinstance(self.v, float) else variables

    def getNew(self):
        v = self.v.getNew() if isinstance(self.v, Expression) else self.v
        ft = self.factorTail.getNew()
        sign = self.sign
        return Factor(sign=sign, v=v, ft=ft)

    def __eq__(self, other):
        if self.__class__ != other.__class__:return False
        if self.v == other.v and self.factorTail == other.factorTail: return True
        return False

    def __neg__(self):
        if isinstance(self.sign, Empty):
            return Factor(self.v,'-', ft= self.factorTail)
        else:
            return Factor(self.v, ft = self.factorTail)

    def __str__(self):
        return f'({self.sign}{self.v}){self.factorTail}' if isinstance(self.v, Expression) else f'{self.sign}{self.v}{self.factorTail}'

    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.v)},{repr(self.factorTail)})'


class FactorTail(object):
    def __init__(self, f):
        self.factor = f

    def eval(self, left, values):
        fator = self.factor.eval(values)
        return left**fator

    def canonicalize(self, left):
        factor = self.factor.canonicalize()
        factorTail = FactorTail(factor)
        if isinstance(left.v, float):
            if isinstance(factor.v, float):
                v = left.pow(factor)
                return Factor(v=v, sign=left.sign)
        if isinstance(left.getValue(),Expression):
            result = left.getValue()
            if factor.v == 2:
                for _ in range(int(factor.v)-1):
                    result = result.mulTerm(left.getValue())
                    result = result.canonicalize()
                return Factor(result)
        return Factor(left.v, sign=left.sign, ft=factorTail)

    def getDerivative(self, symbol):
        factorTail = FactorTail(Factor(self.factor.getValue() -1) )
        return self.factor.getValue(), factorTail
    
    def comparePriority(self,factorTail):
        if isinstance(self.factor.getValue(), Factor) and isinstance(factorTail.factor.getValue(), Factor):
            left = self.factor.getValue()
            right = factorTail.factor.getValue()
            if left > right: False
        elif isinstance(self.factor.getValue(), Factor): return False
        elif  isinstance(factorTail.factor.getValue(), Factor): return True
        elif self.factor.getValue() > factorTail.factor.getValue(): True
        return False

    def add(self,factorTail):
        self.factor.add(factorTail.factor)
        return self

    def getValue(self):
        return self.factor.getValue()

    def getNew(self):
        factor = self.factor.getNew()
        return FactorTail(factor)
        
    def __eq__(self, factorTail):
        if self.__class__ != factorTail.__class__:return False
        if not isinstance(self.factor.getValue(),float) or not isinstance(factorTail.factor.getValue(),float): return False
        if self.factor == factorTail.factor: return True
        return False

    def __neg__(self):
        self.factor = -self.factor
        return self

    def __str__(self):
        return '' if self.factor.v == 1 and isinstance(self.factor.sign, Empty) else f'^{self.factor}' 

    def __repr__(self):
        return f'FactorTail({repr(self.factor)})'


class Variable(object):
    def __init__(self,symbol):
        self.name = symbol
        self.value = None

    def eval(self, values):
        return values[self.name]

    def canonicalize(self):
        return self

    def getDerivative(self, symbol):
        return self, Empty()

    def isDifferentiable(self,symbol):
        if self.name == symbol: return True
        return False
    
    def getVariables(self,variables):
        variables.add(self.name)
        return variables

    def __eq__(self,variable):
        if self.__class__ != variable.__class__:return False
        return True if self.name == variable.name else False

    def insert(self,value):
        self.value = float(value)
        return True

    def __str__(self):
        return f'{str(self.name)}'

    def __repr__(self):
        return f'Variable({repr(self.name)})'


class Sin(object):
    def __init__(self, value):
        self.value = value
    
    def eval(self, values):
        value = self.value if isinstance(self.value,float) else self.value.eval(values)
        return math.sin(value)

    def canonicalize(self):
        value = self.value.canonicalize()
        return Sin(value)

    def isDifferentiable(self,symbol):
        return False

    def getDerivative(self, symbol):
        return self, Empty()

    def getVariables(self, variables):
        return self.value.getVariables(variables)

    def __eq__(self,other):
        if self.__class__ != other.__class__:return False
        if str(self) == str(other): return True

    def __str__(self):
        return f'sin({self.value})'

    def __repr__(self):
        return f'sin({repr(self.value)})'


class Cos(object):
    def __init__(self, value):
        self.value = value
    
    def eval(self, values):
        value = self.value if isinstance(self.value,float) else self.value.eval(values)
        return math.cos(value)

    def canonicalize(self):
        value = self.value.canonicalize()
        return Cos(value)

    def isDifferentiable(self,symbol):
        return False    

    def getDerivative(self, symbol):
        return self, Empty()

    def getVariables(self, variables):
        return self.value.getVariables(variables)

    def __eq__(self,other):
        if self.__class__ != other.__class__:return False
        if str(self) == str(other): return True

    def __str__(self):
        return f'cos({self.value})'  

    def __repr__(self):
        return f'cos({repr(self.value)})'


class Log(object):
    def __init__(self, base, value):
        self.base = base
        self.value = value

    def eval(self, values):
        base = self.base if isinstance(self.base,float) else self.base.eval(values)
        value =  self.value.eval(values)
        return math.log(value)/math.log(base)

    def canonicalize(self):
        base = self.base.canonicalize() if not isinstance(self.base, float) else self.base
        value = self.value.canonicalize()
        return Log(base,value)

    def getDerivative(self,symbol):
        #f(g(x)) = f'(g(x)) * g(x)'
        return self, Empty()

    def isDifferentiable(self,symbol):
        return self.value.isDifferentiable(symbol)

    def getVariables(self, variables):
        return self.value.getVariables(variables)

    def __eq__(self,other):
        if self.__class__ != other.__class__:return False
        if str(self) == str(other): return True
        return False

    def __str__(self):
        return f'log({self.base},{self.value})'
    
    def __repr__(self):
        return f'log({self.base},{self.value})'


class ConstantE(object):
    def __init__(self):
        self.value = math.e
    
    def __str__(self):
        return 'e'

    def __repr__(self):
        return 'e'


class Pi(object):
    def __init__(self):
        self.value = math.pi
    
    def __str__(self):
        return 'pi'

    def __repr__(self):
        return 'pi'


class Constant(Factor):
    def __init__(self,v=Empty(),ft = Empty()):
        super().__init__(self)
        self.v = v
        self.factorTail = ft

    def eval(self, values):
        return 1

    def canonicalize(self):
        return self

    def getDerivative(self, symbol):
        return 1, Empty()

    def isDifferentiable(self,symbol):
        return False

    def compareEquality(self,other):
        if self.__class__ != other.__class__: return False
        return True

    def compareFactorMultiplyPrecedence(self,factor):
        return 0

    def compareFactorPrecedence(self,factor):
        compare = self.compareEquality(factor)
        if compare == 0: return 0
        left = str(self)
        right = str(factor)
        if left > right: return 1
        return -1

    def getVariables(self, variables):
        return variables

    def getValue(self):
        return self.v

    def getNew(self):
        return self

    def __eq__(self,other):
        if self.__class__ != other.__class__: return False
        return True

    def __len__(self):
        return 0

    def __str__(self):
        return f'{self.factorTail}'

    def __repr__(self):
        return f'Constant({repr(self.factorTail)})'
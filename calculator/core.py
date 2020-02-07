import math

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
    
    def canonicalize(self,left):
        return left
    
    def __str__(self):
        return ''
    def __repr__(self):
        return f'Empty'

class Expression(object):
    def __init__(self,t, et=Empty()):
        self.term = t
        self.expressionTail = et
    
    def canonicalize(self):
        # t, et = self.expressionTail.canonicalize(self.term.canonicalize())
        # return Expression(t,et)
        return self.expressionTail.canonicalize(Expression(self.term.canonicalize()))
        # self.term = self.term.canonicalize()
        # self.expressionTail = self.expressionTail.canonicalize(self.term)
        # return self
    def getTerm(self):
        return self.term
    
    def getNextExpr(self):
        return self.expressionTail
    def insertTerm(self, term):
        if isinstance(self.term, Empty):
            return Expression(term)
        else:
            if isinstance(self.expressionTail,Empty):
                if isinstance(term, Term):
                    term = ExpressionTail(term)
                et = term
            else:
                et = self.expressionTail.insertTail(term)
            return Expression(self.term,et)

    def __str__(self):
        return f'{str(self.term)}{str(self.expressionTail)}'
    def __repr__(self):
        return f'Expr({repr(self.term)}, {repr(self.expressionTail)})'


class ExpressionTail(object):
    def __init__(self,t,op='+',et=Empty()):
        self.op = op
        self.term = t
        self.expressionTail = et

    def canonicalize(self, left):
        # right = self.term.canonicalize()
        # left = self.addTerm(left,right)
        # return self.expressionTail.canonicalize(left)
        right = self.term.canonicalize()
        left = self.calc(self.op,left,right)
        result = self.expressionTail.canonicalize(left)
        # return Expression(left,self)
        # return self
        return result

    
    def calc(self, op, expr, term):
        left_term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        et = Empty()
        if isinstance(nextExpr, Empty):
            if left_term == term:
                left_term = left_term.add(term)
            else:
                et = ExpressionTail(term)
            return Expression(left_term,et)
        else:
            result = Expression(Empty())
            flag = True
            while True:
                if left_term == term:
                    left_term = left_term.add(term)
                    result = result.insertTerm(left_term)
                    result = result.insertTerm(nextExpr)
                    flag = False
                    break
                else:
                    result = result.insertTerm(left_term)
                    left_term = nextExpr.term if isinstance(nextExpr, ExpressionTail) else Empty()
                    nextExpr = nextExpr.expressionTail
                    if isinstance(left_term, Empty): break
            # result = result.insertTerm(left_term)
            if flag: result = result.insertTerm(term)
            return result
        # ----------------------------------------------------
        # # nextExpr = None
        # while not isinstance(nextExpr, Empty):
        #     # nextExpr = expr.getNextExpr()
        #     if op == '+':
        #         if left_term == term:
        #             left_term = left_term.add(term)
        #             return Expression(left_term,nextExpr)
        #         else:
        #             pass
        #             # return Expression(terms,Empty())
        #         # et = ExpressionTail('+',term,Empty())
        #     else:
        #         if left_term == term:
        #             left_term = left_term.sub(term)
        #         pass
        #     left_term = nextExpr.term
        #             # return left_term
        #             # return Expression(terms,Empty())
        #         # et = ExpressionTail('-',term,Empty())
        #     # return Expression(terms,et)
        

    def insertTail(self,term):
        if isinstance(self.expressionTail, Empty):
            et = ExpressionTail(term)
            return ExpressionTail(self.term, et)
        else:
            return self.expressionTail.insertTail(term)

    def __str__(self):
        return f'{str(self.op)}{str(self.term)}{str(self.expressionTail)}'
    def __repr__(self):
        return f'ExprTail({self.op}, {repr(self.term)}, {repr(self.expressionTail)})'

class Term(object):
    def __init__(self, f, tt = Empty()):
        self.factor = f
        self.termTail = tt

    def canonicalize(self):
        #empty이면 term이 리턴되어야 하기 때문에 term을 감싸야함
        return self.termTail.canonicalize(Term(self.factor.canonicalize()))
        # return self.termTail.canonicalize(Term(Factor(self.factor.canonicalize())))

    def add(self, term):
        result = self.factor.add(term.factor)
        return Term(result,self.termTail)
    
    def sub(self, term):
        result = self.factor.sub(term.factor)
        return Term(result,self.termTail)
    
    def getFactor(self):
        return self.factor

    def getNextTerm(self):
        return self.termTail

    def __eq__(self,term):
        if self.factor == term.factor:
            if self.termTail == term.termTail:
                return True
        return False

    def __str__(self):
        return f'{str(self.factor)}{str(self.termTail)}'
    def __repr__(self):
        return f'Term({repr(self.factor)},{repr(self.termTail)})'

class TermTail(object):
    def __init__(self, op ='*', f = Empty(), tt = Empty()):
        self.op = op
        self.factor = f
        self.termTail = tt


    def canonicalize(self, left):
        # right = self.factor.canonicalize()
        # left = self.mulFactor(left,right)
        # return self.termTail.canonicalize(left)
        left = left.factor
        # right = self.factor.canonicalize()
        # left = mulFactor(left,right)
        self.factor = self.factor.canonicalize()
        return Term(left,self)

    def mulFactor(self, factors, factor):
        return Term()
        # # termTail = TermTail('*',Empty(), Empty())
        # result = Term(Empty(),Empty())
        # left = factors

        # while left.getNextTerm is not Empty():
        #     left_factor = left.getFactor()
        #     left = left.getNextTerm()
        #     compare = left_factor.comparePrecedence(factor)
        #     if compare > 0:
        #         pass
        #     elif compare == 0:
        #         left_factor = left_factor.__mul__(factor)
        #     else:
        #         result.factor = left_factor
        #         result = result.termTail
        # return result

    def __eq__(self, termTail):
        if isinstance(termTail, Empty): return False
        if self.factor == termTail.factor:
            if self.termTail == termTail.termTail:
                return True
        return False

    def __str__(self):
        return f'{self.op}{str(self.factor)}{str(self.termTail)}'
    def __repr__(self):
        return f'TermTail({self.op},{repr(self.factor)},{repr(self.termTail)})'

class Factor(object):
    def __init__(self, v, sign = Empty(), ft = Empty()):
        self.sign = sign
        self.v = v
        self.factorTail = ft
    
    def canonicalize(self):

        v = self.v.canonicalize() if not isinstance(self.v,float) else self.v
        if not isinstance(v, Factor):
            v = Factor(v)
        v = self.factorTail.canonicalize(v)
        if self.sign == '-':
            v = -v
        return v

    def add(self,factor):
        left = self.v
        right = factor.v
        if self.sign == '-':
            left = -left
        if factor.sign == '-':
            right = -right
        result = left + right
        result_sign = Empty()
        if result < 0:
            result_sign = '-'
        result = abs(result)
        
        return Factor(result,result_sign, self.factorTail)

    def sub(self,factor):
        left = self.v
        right = factor.v
        if self.sign == '-':
            left = -left
        if factor.sign == '-':
            right = -right
        result = left - right
        result_sign = Empty()
        if result < 0:
            result_sign = '-'
        result = abs(result)
        
        return Factor(result,result_sign, self.factorTail)

    def __eq__(self, factor):
        if self.v.__class__ == factor.v.__class__ and self.factorTail == factor.factorTail: return True
        return False
    
    def __neg__(self):
        if isinstance(self.sign, Empty):
            return Factor(self.v,'-', self.factorTail)
        else:
            return Factor(self.v, ft = self.factorTail)
    
    def __str__(self):
        return f'({self.sign}{self.v}{self.factorTail})' if isinstance(self.v, Expression) else f'{self.sign}{self.v}{self.factorTail}'
    def __repr__(self):
        return f'Factor({repr(self.sign)},{repr(self.v)},{repr(self.factorTail)})'

class FactorTail(object):
    def __init__(self, v, ft = Empty()):
        self.v = v
        self.factorTail = ft

    def canonicalize(self, left):
        return Factor(left, self)

    def __eq__(self, factorTail):
        if self.v == factorTail.v and self.factorTail == factorTail.factorTail: return True
        return False
    def __str__(self):
        return f'{self.v}'
    def __repr__(self):
        return f'FactorTail({self.v})'

class Value(object):
    def __init__(self, e):
        self.e = e

    def __eq__(self, value):
        if self.e == value.e: return True
        return False

    def canonicalize(self):
        if isinstance(self.e, float): return self
        return Value(self.e.canonicalize())

    def __str__(self):
        return f'{self.e}'
    def __repr__(self):
        return f'Value({repr(self.e)})'


class Variable(object):
    def __init__(self,symbol):
        self.name = symbol
    
    def __eq__(self,variable):
        if self.name == variable.name: return True
        return False
    def canonicalize(self):
        return self
    def __str__(self):
        return f'{self.name}'
    def __repr__(self):
        return f'Variable({self.name})'

class Sin(object):
    pass

class Cos(object):
    pass

class Log(object):
    def __init__(self, base, value):
        self.base = base
        self.value = value
    
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
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
    def add(self,left):
        return left
    def __eq__(self,other):
        return self.__class__ == other.__class__
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
            return self.insertExprTail(term)

    def insertExprTail(self, term):
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
        if self.op == '-':
            self.term = -self.term
            self.op = '+'
        
        right = self.term.canonicalize()
        left = self.calc(self.op,left,right)
        result = self.expressionTail.canonicalize(left)
        # return Expression(left,self)
        # return self
        return result

    # #더하기, 빼기, insert하기
    # def calc(self, op, expr, term):
    #     left_term = expr.getTerm()
    #     nextExpr = expr.getNextExpr()
    #     result = Expression(Empty())
    #     noSameTerm = True
    #     while not isinstance(left_term, Empty):
    #         #우선순위 파악하는걸로 수정해야함
    #         # if left_term == term:
    #         compare = left_term.compareEquality(term)
    #         if compare == 0:
    #             left_term = left_term.add(term)
    #             result = result.insertTerm(left_term)
    #             result = result.insertExprTail(nextExpr)
    #             noSameTerm = False
    #             break  
    #         elif compare == 1:
    #             result = result.insertTerm(term)
    #             result = result.insertTerm(left_term)
    #             result = result.insertExprTail(nextExpr)
    #             noSameTerm = False
    #             break
    #         else:
    #             result = result.insertTerm(left_term)
    #             left_term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
    #             nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
    #     if noSameTerm: result = result.insertTerm(term)
    #     return result
    
        #더하기, 빼기, insert하기
    def calc(self, op, expr, term):
        left_term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        result = Expression(Empty())
        noSameTerm = True
        while not isinstance(left_term, Empty):
            #우선순위 파악하는걸로 수정해야함
            # if left_term == term:
            compare = left_term.compareEquality(term)
            if compare == 0:
                left_term = left_term.add(term)
                result = result.insertTerm(left_term)
                result = result.insertExprTail(nextExpr)
                noSameTerm = False
                break  
            else:
                result = result.insertTerm(left_term)
                left_term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
                nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        if noSameTerm: result = result.insertTerm(term)
        return result
        
    def getTerm(self):
        return self.term
    def getNextExpr(self):
        return self.expressionTail
    def insertTail(self,term):
        if isinstance(self.expressionTail, Empty):
            if isinstance(term, Term):
                term = ExpressionTail(term)
            
            return ExpressionTail(self.term, et=term)
        else:
            return self.expressionTail.insertTail(term)

    def __str__(self):
        return f'{str(self.op)}{str(self.term)}{str(self.expressionTail)}'
    def __repr__(self):
        return f'ExprTail({repr(self.op)}, {repr(self.term)}, {repr(self.expressionTail)})'

class Term(object):
    def __init__(self, f,tt = Empty(),coeff = 1.0):
        self.coefficient = coeff
        self.factor = f
        self.termTail = tt

    def canonicalize(self):
        #empty이면 term이 리턴되어야 하기 때문에 term을 감싸야함
        return self.termTail.canonicalize(Term(self.factor.canonicalize()))
        # return self.termTail.canonicalize(Term(Factor(self.factor.canonicalize())))

    # def 

    def add(self, term):
        if isinstance(self.factor.v, float) and isinstance(term.factor.v, float):
        # if isinstance(self.factor, float) and isinstance(term.factor, float):
            result = self.factor.add(term.factor)
            return Term(result,self.termTail)
        else:
            my_sign = self.factor.getSign()
            term_sign = term.factor.getSign()
            if my_sign == '-':
                self.coefficient = -self.coefficient
                self.factor.sign = Empty()
            if term_sign == '-':
                term.coefficient = -term.coefficient
                term.factor.sign = Empty()
            coeff = self.coefficient+term.coefficient
            if coeff == 0:
                return Term(Factor(0.0))
            return Term(self.factor, self.termTail, coeff = coeff)
    #이제 안씀
    def sub(self, term):
        result = self.factor.sub(term.factor)
        return Term(result,self.termTail)
    
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
                res = left_f.compareEquality(right_f)
                if res != 0: return -1
                left = left.getNextTerm()
                right = right.getNextTerm()
            return 0
        return -1

        # result = self.factor.compareFactorPrecedence(term.factor)
        # return result

    def insertFactor(self,factor):
        if isinstance(self.factor, Empty):
            return Term(factor,self.termTail)
        else:
            if isinstance(self.termTail, Empty):
                tt = TermTail(f=factor)
                if isinstance(factor,Empty):
                    tt = factor
                return Term(self.factor,tt)
            else:
                tt = self.termTail.insertTail(factor)
                return Term(self.factor,tt)
            
    def compareTermPrecedence(self, term):
        result = self.factor.compareFactorPrecedence(term.factor)
        return result

    def __eq__(self,term):
        if self.factor == term.factor:
            if self.termTail == term.termTail:
                return True
        return False
    def __neg__(self):
        f = -self.factor
        return Term(f,self.termTail)
    
    def __len__(self):
        result = 1
        result += len(self.termTail)
        return result

    def __str__(self):
        return f'{self.coefficient}*{str(self.factor)}{str(self.termTail)}' if self.coefficient != 1 else f'{str(self.factor)}{str(self.termTail)}'
    def __repr__(self):
        return f'Term({self.coefficient},{repr(self.factor)},{repr(self.termTail)})'

class TermTail(object):
    def __init__(self, op ='*', f = Empty(), tt = Empty()):
        self.op = op
        self.factor = f
        self.termTail = tt


    def canonicalize(self, left):
        right = self.factor.canonicalize()
        left = self.calc(self.op, left, right)
        return left
    
    def calc(self,op,factors,factor):
        left_factor = factors.getFactor()
        nextFactor = factors.getNextTerm()
        result = Term(Empty())
        noSameFactor = True
        while not isinstance(left_factor, Empty):
            compare = left_factor.compareFactorPrecedence(factor)
            if compare == 0:
                left_factor = left_factor.mul(factor)
                result = result.insertFactor(left_factor)
                result = result.insertFactor(nextFactor)
                noSameFactor = False
                break
            elif compare == 1:
                result = result.insertFactor(factor)
                result = result.insertFactor(left_factor)
                result = result.insertFactor(nextFactor)
                noSameFactor = False
                break
            else:
                result = result.insertFactor(left_factor)
                left_factor = nextFactor.getFactor() if isinstance(nextFactor, TermTail) else Empty()
                nextFactor = nextFactor.getNextTerm() if isinstance(nextFactor, TermTail) else Empty()
        if noSameFactor: result = result.insertFactor(factor)
        return result
    
    def mulFactor(self, factor):
        pass
            

    def getFactor(self):
        return self.factor
    def getNextTerm(self):
        return self.termTail
    def insertTail(self,factor):
        if isinstance(self.termTail,Empty):
            tt = TermTail(f=factor)
            if isinstance(factor,Empty):
                tt = factor
            return TermTail(f=self.factor,tt=tt)
        else:
            tt = self.termTail.insertTail(factor)
            return TermTail(f=self.factor,tt=tt)
    
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
    
    def canonicalize(self):
        #factor은 factor을 리턴해야함
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
    
    def mul(self,factor):
        if isinstance(self.v,float) and isinstance(factor.v,float):
            v = self.v * factor.v
            return Factor(v=v)
        factorTail = self.factorTail.add(factor.factorTail)
        return Factor(v=self.v,ft=factorTail)
    
    #안씀
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
    def compareFactorPrecedence(self,factor):

        left = self.getPriority()
        right = factor.getPriority()
        if left < right: return 1
        elif left == right: return 0
        else: return -1
    
    def getPriority(self):
        result = 0
        if isinstance(self.v, Variable):
            result += 1
        if isinstance(self.factorTail, FactorTail):
            result += self.factorTail.getPriority()
        return result
    
    def compareEquality(self,factor):
        if self == factor: return 0
        else: return -1
    def getSign(self):
        return self.sign

    def __eq__(self, other):
        if isinstance(self.v, float) and isinstance(other.v,float):return True
        if self.v == other.v and self.factorTail == other.factorTail: return True
        return False
    
    def __neg__(self):
        if isinstance(self.sign, Empty):
            return Factor(self.v,'-', ft= self.factorTail)
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
        # return Factor(left, self)
        v = self.factorTail.canonicalize(self.v)
        if isinstance(left.v, float):
            v = left.v**v.v
            return Factor(v)
        else:
            return Factor(left.v,self)
    def getPriority(self):
        result = 0
        result += self.factorTail.getPriority()
        result += self.v
        return result
    def add(self,factorTail):
        result = self.v.add(factorTail.v)
        return FactorTail(result)

    def __eq__(self, factorTail):
        if self.v == factorTail.v and self.factorTail == factorTail.factorTail: return True
        return False
    def __str__(self):
        return f'^{self.v}{self.factorTail}'
    def __repr__(self):
        return f'FactorTail({repr(self.v)},{self.factorTail})'

# class Value(object):
#     def __init__(self, e):
#         self.e = e

#     def __eq__(self, value):
#         if self.e == value.e: return True
#         return False

#     def canonicalize(self):
#         if isinstance(self.e, float): return self
#         return Value(self.e.canonicalize())

#     def __str__(self):
#         return f'{self.e}'
#     def __repr__(self):
#         return f'Value({repr(self.e)})'


class Variable(object):
    def __init__(self,symbol):
        self.name = symbol
    
    def __eq__(self,variable):
        if self.__class__ != variable.__class__:return False
        return True if self.name == variable.name else False

    def canonicalize(self):
        return self
    def __str__(self):
        return f'{str(self.name)}'
    def __repr__(self):
        return f'Variable({repr(self.name)})'

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
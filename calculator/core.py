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
    def compareEquality(self,other):
        if self.__class__ == other.__class__: return 0
        else: return -1
    def compareFactorPrecedence(self,other):
         return -1

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
        return self.expressionTail.canonicalize(Expression(self.term.canonicalize()))
    
    def mulTerm(self,term):
        left_term = self.getTerm()
        nextExpr = self.getNextExpr()
        result = Expression(Empty)
        while not isinstance(left_term, Empty):
            print(left_term)
            res = left_term.mul(term)
            result.insertTerm(res)
            left_term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
            nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        return result
    
    
    
    def getTerm(self):
        return self.term
    
    def getNextExpr(self):
        return self.expressionTail
    
    def insertTerm(self, term):
        """
        input:term output: expression
        inserting term
        """
        if isinstance(self.term, Empty):
            return Expression(term)
        else:
            return self.insertExprTail(ExpressionTail(t=term))

    def insertExprTail(self, expressionTail):
        if isinstance(self.expressionTail,Empty):
            return Expression(self.term,expressionTail)
        else:
            et = self.expressionTail.insertTail(expressionTail)
        return Expression(self.term,et)
    
    def dropZero(self, expr):
        term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        result = Expression(Empty())
        allZero = True
        while not isinstance(term, Empty):
            if term.coefficient != 0:
                result = result.insertTerm(term)
                allZero = False
            term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
            nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        if allZero: result = Expression(Term(Constant(),coeff = 0))
        return result


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
        if self.op == '-':
            self.term = -self.term
            self.op = '+'
        
        right = self.term.canonicalize()
        left = self.calc(self.op,left,right)
        result = self.expressionTail.canonicalize(left)
        return result

    #더하기, 빼기, insert하기
    def calc(self, op, expr, term):
        left_term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        result = Expression(Empty())
        noSameTerm = True
        while not isinstance(left_term, Empty):
            compare = left_term.compareTermPrecedence(term)
            if compare == 0:
                left_term = left_term.add(term)
                result = result.insertTerm(left_term)
                result = result.insertExprTail(nextExpr)
                noSameTerm = False
                break  
            elif compare == 1:
                result = result.insertTerm(term)
                result = result.insertTerm(left_term)
                result = result.insertExprTail(nextExpr)
                noSameTerm = False
                break
            else:
                result = result.insertTerm(left_term)
                left_term = nextExpr.getTerm() if isinstance(nextExpr, ExpressionTail) else Empty()
                nextExpr = nextExpr.getNextExpr() if isinstance(nextExpr, ExpressionTail) else Empty()
        if noSameTerm: result = result.insertTerm(term)
        result = result.dropZero(result)
        return result
    
        
    def getTerm(self):
        return self.term
    def getNextExpr(self):
        return self.expressionTail
    def insertTail(self,expressionTail):
        if isinstance(self.expressionTail, Empty):
            return ExpressionTail(self.term, et=expressionTail)
        else:
            et = self.expressionTail.insertTail(expressionTail)
            return ExpressionTail(self.term, et=et)

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
        factor = self.factor.canonicalize()
        if factor.sign == '-':
            self.coefficient = -self.coefficient
            factor.sign = Empty()
        if isinstance(factor.getValue(), float):
            self.coefficient *= factor.getValue()
            # factor = Factor(1.0)
            # factor = Factor(Empty())
            # factor = Empty()
            factor = Constant()
        return self.termTail.canonicalize(Term(f=factor,coeff=self.coefficient))
    
    def add(self, term):
        # my_sign = self.factor.getSign()
        # term_sign = term.factor.getSign()
        # if my_sign == '-':
            # self.coefficient = -self.coefficient
            # self.factor.sign = Empty()
        # if term_sign == '-':
            # term.coefficient = -term.coefficient
            # term.factor.sign = Empty()
        coeff = self.coefficient+term.coefficient
        if coeff == 0:
            return Term(Factor(1.0),coeff=coeff)
        return Term(self.factor, self.termTail, coeff = coeff)
    def mul(self, term):
        coeff = self.coefficient * term.coefficient
        termTail = TermTail(f=term.getFactor())
        self.coefficient = coeff
        result = termTail.canonicalize(self)
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
                # if isinstance(left_f, Empty):return False
                res = left_f.compareEquality(right_f)
                if res != 0: return False
                left = left.getNextTerm()
                right = right.getNextTerm()
            return True
        return False

    def insertFactor(self,factor):
        """
        input:factor output: Term
        inserting factor
        """
        if isinstance(self.factor, Empty):
            return Term(factor,self.termTail,coeff=self.coefficient)
        else:
            return self.insertTermTail(TermTail(f=factor))

    def insertTermTail(self, termTail):
        """
        input:termtail output: Term
        inserting termtail
        """
        if isinstance(self.termTail, Empty):
            return Term(self.factor, termTail, coeff=self.coefficient)
        else:
            tt = self.termTail.insertTail(termTail)
            return Term(self.factor,tt,coeff=self.coefficient)
    
    def compareTermPrecedence(self, term):
        equal = self.compareEquality(term)
        if equal: return 0
        return self.factor.compareFactorPrecedence(term.factor)
        # if self.factor < term.factor:return -1
        # else: return 1

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
        if isinstance(self.factor,Constant):
            return f'{self.coefficient}{str(self.termTail)}'
        return f'{self.coefficient}*{str(self.factor)}{str(self.termTail)}' if self.coefficient != 1 else f'{str(self.factor)}{str(self.termTail)}'
    def __repr__(self):
        return f'Term({self.coefficient},{repr(self.factor)},{repr(self.termTail)})'

class TermTail(object):
    def __init__(self, op ='*', f = Empty(), tt = Empty()):
        self.op = op
        self.factor = f
        self.termTail = tt


    def canonicalize(self, left):
        right = self.factor
        if self.op == '/':
            right = right.makeFactorTailNeg()
            self.op = '*'
        right = right.canonicalize()
        left = self.calc(left, right)
        result = self.termTail.canonicalize(left)
        return result
    
    def calc(self, factors,factor):
        coeff = factors.coefficient
        if isinstance(factor.getValue(),float):
            #coeff에 연산
            coeff = coeff*factor.getValue()
            factors.coefficient = coeff
            if coeff == 0: return Term(Factor(Empty),coeff=0)
            return factors
        
        elif isinstance(factor.getValue(), Expression):
            expr = factor.getValue()
            res = expr.mulTerm(factors)
            return res
        else:
            left_factor = factors.getFactor()
            nextFactor = factors.getNextTerm()
            result = Term(Empty(),coeff=coeff)
            noSameFactor = True
            while not isinstance(left_factor, Empty):
                compare = left_factor.compareFactorPrecedence(factor)
                if compare == 0:
                    left_factor = left_factor.mul(factor)
                    result = result.insertFactor(left_factor)
                    result = result.insertTermTail(nextFactor)
                    noSameFactor = False
                    break
                elif compare == 1:
                    result = result.insertFactor(factor)
                    result = result.insertFactor(left_factor)
                    result = result.insertTermTail(nextFactor)
                    noSameFactor = False
                    break
                else:
                    result = result.insertFactor(left_factor)
                    left_factor = nextFactor.getFactor() if isinstance(nextFactor, TermTail) else Empty()
                    nextFactor = nextFactor.getNextTerm() if isinstance(nextFactor, TermTail) else Empty()
            if noSameFactor: result = result.insertFactor(factor)
            return result
    def getFactor(self):
        return self.factor
    def getNextTerm(self):
        return self.termTail
    def insertTail(self,termTail):
        if isinstance(self.termTail,Empty):
            return TermTail(f=self.factor,tt=termTail)
        else:
            tt = self.termTail.insertTail(termTail)
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
        if factorTail.factor.getValue() == 0: return Constant()
        return Factor(v=self.v,ft=factorTail)

        
        return Factor(result,result_sign, self.factorTail)
    
    
    def compareFactorPrecedence(self,factor):
        compare = self.compareEquality(factor)
        if compare == 0: return 0
        left = str(self)
        right = str(factor)
        if left > right: return -1
        else:return 1

    
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
    def makeFactorTailNeg(self):
        if isinstance(self.factorTail,Empty):
            self.factorTail = FactorTail(f=Factor(1.0),ft=Empty())
        self.factorTail = -self.factorTail
        return self
    def getSign(self):
        return self.sign
    def pow(self,factor):
        if factor.sign == '-':
            factor.v = -factor.v
        return self.v**factor.v

    def getValue(self):
        return self.v
    def __eq__(self, other):
        if self.__class__ != other.__class__:return False
        # if isinstance(self.v, float) and isinstance(other.v,float):return True
        if isinstance(other,Empty):return False
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
    def __init__(self, f, ft = Empty()):
        self.factor = f
        self.factorTail = ft

    def canonicalize(self, left):
        factor = self.factorTail.canonicalize(self.factor)
        if isinstance(left.v, float):
            if isinstance(factor.v, float):
                v = left.pow(factor)
                return Factor(v=v)
        return Factor(left.v,ft=self)
    #안씀
    def getPriority(self):
        result = 0
        result += self.factorTail.getPriority()
        result += self.factor.v
        return result
    
    def add(self,factorTail):
        result = self.factor.add(factorTail.factor)
        return FactorTail(result)

    def __eq__(self, factorTail):
        if self.__class__ != factorTail.__class__:return False
        if self.factor == factorTail.factor and self.factorTail == factorTail.factorTail: return True
        return False
    def __neg__(self):
        self.factor = -self.factor
        return self
    def __str__(self):
        return '' if self.factor.v == 1 and isinstance(self.factor.sign, Empty) else f'^{self.factor}{self.factorTail}' 
    def __repr__(self):
        return f'FactorTail({repr(self.factor)},{repr(self.factorTail)})'


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
    def __init__(self, value):
        self.value = value
    
    def canonicalize(self):
        self.value = self.value.canonicalize()
        return self
    
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
    
    def canonicalize(self):
        self.value = self.value.canonicalize()
        return self
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
    
    def canonicalize(self):
        self.value = self.value.canonicalize()
        return self
    
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

class Constant(object):
    def compareEquality(self,other):
        if self.__class__ == other.__class__: return 0
        else: return -1
    def compareFactorPrecedence(self,other):
        return -1

    def __len__(self):
        return 0
    def __str__(self):
        return ''
    def __repr__(self):
        return 'Constant'
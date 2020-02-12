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
    def eval(self,left):
        return left
    def canonicalize(self,left):
        return left
    def add(self,left):
        return left
    def compareEquality(self,other):
        if self.__class__ == other.__class__: return 0
        return -1
    # def compareFactorPrecedence(self,other):
    #      return -1
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
    def eval(self):
        return self.expressionTail.eval(self.term.eval())
    def canonicalize(self):
        term = self.term.canonicalize()
        #term이 expression일때 최종 expression에 확장
        if isinstance(term.getFactor().getValue(),Expression) and term.getFactor().factorTail.factor.sign != '-' and len(term) == 1 and term.coefficient == 1:
            temp_expr = term.getFactor().getValue()
            if term.coefficient < 0:
                temp_expr = -temp_expr
            term = temp_expr.getTerm()
            temp_et = temp_expr.getNextExpr()
            self.expressionTail = temp_et.insertTail(self.expressionTail) if not isinstance(temp_et, Empty) else self.expressionTail
        return self.expressionTail.canonicalize(Expression(term))
    
    def mulTerm(self,term):
        #term 또는 expr n번 반복
        right_term = term
        right_nextExpr = Empty()
        if isinstance(term.getFactor().getValue(), Expression)  and term.getFactor().factorTail.factor.sign != '-':
            right_expr = term.getFactor().getValue()
            # if term.getFactor().sign == '-':
            right_term = right_expr.getTerm()
            right_nextExpr = right_expr.getNextExpr()
        result = Expression(Empty())
        while not isinstance(right_term, Empty):
            left_term = self.getTerm()
            left_nextExpr = self.getNextExpr()
            # sub_result = Expression(Empty)
            while not isinstance(left_term, Empty):
                res = left_term.mul(right_term)
                result = result.insertTerm(res)
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
    def __init__(self,t,op='+',et=Empty()):
        self.op = op
        self.term = t
        self.expressionTail = et
    def eval(self, left):
        right = self.term.eval()
        left = left+right
        return self.expressionTail.eval(left)
    def canonicalize(self, left):
        if self.op == '-':
            self.term = -self.term
            self.op = '+'
           
        right = self.term.canonicalize()
        if isinstance(right.getFactor().getValue(),Expression)  and right.getFactor().factorTail.factor.sign != '-':
            temp_expr = right.getFactor().getValue()
            if right.coefficient < 0:
                temp_expr = -temp_expr
            right = temp_expr.getTerm()
            self = self.insertTail(temp_expr.getNextExpr())
        
        left = self.calc(left,right)
        result = self.expressionTail.canonicalize(left)
        return result

    #더하기, 빼기, insert하기
    def calc(self, expr, term):
        left_term = expr.getTerm()
        nextExpr = expr.getNextExpr()
        result = Expression(Empty())
        noSameTerm = True
        # if isinstance(left_term.getFactor().getValue(), Expression):
        #     expr = left_term.getFactor().getValue()
        #     temp = expr.addTerm(term)
        #     return temp
        
        
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
    def eval(self):
        result = self.coefficient * self.factor.eval()
        return self.termTail.eval(result)
    def canonicalize(self):
        #empty이면 term이 리턴되어야 하기 때문에 term을 감싸야함
        factor = self.factor.canonicalize()
        if factor.sign == '-':
            self.coefficient = -self.coefficient
            factor.sign = Empty()
        if isinstance(factor.getValue(), float):
            self.coefficient *= factor.getValue()
            factor = Constant( ft=factor.factorTail)
        return self.termTail.canonicalize(Term(f=factor,coeff=self.coefficient))
    
    def add(self, term):
        coeff = self.coefficient+term.coefficient
        if coeff == 0:
            return Term(Factor(1.0),coeff=coeff)
        return Term(self.factor, self.termTail, coeff = coeff)
    
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
                # if isinstance(left_f, Empty):return False
                if not left_f.compareEquality(right_f): return False
                # if res != 0: return False
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
        if self.compareEquality(term): return 0
        left = str(self)
        right = str(term)
        return 1 if left > right else -1

    def pow(self,power_factor):
        coeff = self.coefficient**power_factor
        factor = self.getFactor()
        factor = factor.pow(power_factor)

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

    def eval(self, left):
        right = self.factor.eval()
        left = left*right
        return self.termTail.eval(left)
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
        # print(factors, factor, 'calc')
        coeff = factors.coefficient
        result = Term(Empty(), coeff = coeff)
        # if isinstance(factors.getFactor().getValue(), Expression):
        # if isinstance(factors.getFactor().getValue(), Expression) and factors.getFactor().factorTail.factor.sign != '-':
        #     left_factor = factors.getFactor()
        #     temp_expr = left_factor.getValue()
        #     temp_expr = temp_expr.mulTerm(Term(factor))
        #     temp_expr = temp_expr.canonicalize()
        #     result = result.insertFactor(Factor(v=temp_expr,sign=left_factor.sign, ft=left_factor.factorTail))
        #     return result
        # elif isinstance(factor.getValue(), Expression) and factor.factorTail.factor.sign != '-':
        #     result = Term(Empty())
        #     left_factor = factor
        #     temp_expr = left_factor.getValue()
        #     temp_expr = temp_expr.mulTerm(factors)
        #     temp_expr = temp_expr.canonicalize()
        #     result = result.insertFactor(Factor(v=temp_expr,sign=left_factor.sign, ft=left_factor.factorTail))
        #     return result
        # elif isinstance(factor.getValue(),float):
        if isinstance(factor.getValue(),float):
            #coeff에 연산
            coeff = coeff*factor.getValue()
            factors.coefficient = coeff
            # result.coefficient = coeff
            # result.insertFactor(Constant())
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
                result = result.insertFactor(left_factor)
                result = result.insertTermTail(nextFactor)
                noSameFactor = False
                break
            # # if isinstance(factors.getFactor().getValue(), Expression):
            # elif isinstance(factors.getFactor().getValue(), Expression) and factors.getFactor().factorTail.factor.sign != '-':
            #     left_factor = factors.getFactor()
            #     temp_expr = left_factor.getValue()
            #     temp_expr = temp_expr.mulTerm(Term(factor))
            #     # temp_expr = temp_expr.canonicalize()
            #     result = result.insertFactor(Factor(v=temp_expr,sign=left_factor.sign, ft=left_factor.factorTail))
            #     return result
            # elif isinstance(factor.getValue(), Expression) and factor.factorTail.factor.sign != '-':
            #     result = Term(Empty())
            #     left_factor = factor
            #     temp_expr = left_factor.getValue()
            #     temp_expr = temp_expr.mulTerm(factors)
            #     # temp_expr = temp_expr.canonicalize()
            #     result = result.insertFactor(Factor(v=temp_expr,sign=left_factor.sign, ft=left_factor.factorTail))
            #     return result
            
            
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
    def eval(self):
        v = self.v if isinstance(self.v, float) else self.v.eval()
        return self.factorTail.eval(v)

    def canonicalize(self):
        #factor은 factor을 리턴해야함
        v = self.v.canonicalize() if not isinstance(self.v,float) else self.v
        if isinstance(v, Expression):
            pass
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
        if isinstance(self,Constant): return factor
        # print(self,factor, 'mul')
        # if isinstance(self, Constant):
        #     return factor
        # if isinstance(self.getValue(), Expression):
        #     temp_expr = self.getValue()
        #     temp_expr = temp_expr.mulTerm(Term(factor))
        #     temp_expr = temp_expr.canonicalize()
        #     result = Factor(v=temp_expr,sign=self.sign, ft=self.factorTail)
        #     return result
        # elif isinstance(factor.getValue(), Expression):
        #     left_factor = factor
        #     temp_expr = left_factor.getValue()
        #     temp_expr = temp_expr.mulTerm(Term(Factor(self.v)))
        #     temp_expr = temp_expr.canonicalize()
        #     result = Factor(v=temp_expr,sign=left_factor.sign, ft=left_factor.factorTail)
        #     return result
        factorTail = self.factorTail.add(factor.factorTail)
        # print(factorTail, repr(factorTail), 'mul')
        if factorTail.factor.getValue() == 0: return Constant()
        return Factor(v=self.v,ft=factorTail)

        
        return Factor(result,result_sign, self.factorTail)
    
    
    def compareFactorPrecedence(self,factor):
        # if isinstance(factor, Constant): return 0

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
        # if isinstance(self.getValue(), Expression) or isinstance(factor.getValue(), Expression) : return 0
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
        if self.v == factor.v: return True
        return False
    
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
    def eval(self, left):
        return left**self.factor.eval()
    def canonicalize(self, left):
        # print(left,type(left),'FactorTail')
        self.factor = self.factor.canonicalize()
        
        
        
        if isinstance(left.v, float):
            if isinstance(self.factor.v, float):
                v = left.pow(self.factor)
                return Factor(v=v,sign=left.sign)
        if isinstance(left.getValue(),Expression):
            result = left.getValue()
            if self.factor.v == 2:
                for _ in range(int(factor.v)-1):
                    result = result.mulTerm(left.getValue())
                    result = result.canonicalize()
                return Factor(result)
        return Factor(left.v,sign=left.sign,ft=self)
    #안씀
    def getPriority(self):
        result = 0
        result += self.factorTail.getPriority()
        result += self.factor.v
        return result
    
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
        result = self.factor.add(factorTail.factor)
        return FactorTail(result)

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

    def eval(self):
        return self.value
    def canonicalize(self):
        return self
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
    
    def eval(self):
        value = self.value if isinstance(self.value,float) else self.value.eval()
        return math.sin(value)

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
    
    def eval(self):
        value = self.value if isinstance(self.value,float) else self.value.eval()
        return math.cos(value)
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
    def eval(self):
        base = self.base if isinstance(self.base,float) else self.base.eval()
        value = self.value if isinstance(self.value,float) else self.value.eval()

        return math.log(value)/math.log(base)
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

class Constant(Factor):
    def __init__(self,v=Empty(),ft = Empty()):
        super().__init__(self)
        self.v = v
        self.factorTail = ft
    def getValue(self):
        return self.v
    def eval(self):
        return 1
    def canonicalize(self):
        return self
    def compareEquality(self,other):
        if self.__class__ != other.__class__: return False
        # if self.factorTail != other.factorTail: return False
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
    def __eq__(self,other):
        if self.__class__ != other.__class__: return False
        return True
    def __len__(self):
        return 0
    def __str__(self):
        return f'{self.factorTail}'
    def __repr__(self):
        return f'Constant({repr(self.factorTail)})'
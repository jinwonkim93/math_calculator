import math
from factor_new import Variable, Constant
from mathematical_constant import *
from empty import Empty

def logn(n, x = math.e):
    print(n/x)
    return 1 + logn(n/x, x) if n > (x-1) else 0

def lognNew(n, x = E):
    return math.log(n) / math.log(x)

def triangleFunction(func, expr):
    print(type(expr))
    if func.symbol == 'sin':
        if isinstance(expr, Constant):
            return math.sin(expr.value)
        elif isinstance(expr, float):
            return Constant(math.sin(expr))
        else:
            return func
    elif func.symbol == 'cos':
        if isinstance(expr, Constant):
            return math.cos(expr.value)
        elif isinstance(expr, float):
            return math.cos(expr)
        else:
            return func
    elif func.symbol == 'tan':
        if isinstance(expr, Constant):
            return math.tan(expr.value)
        elif isinstance(expr, float):
            return math.tan(expr)
        else:
            return func
"""
def pow(base,expo):
    if isinstance(base, Variable):
        new_expo = Empty()
        if isinstance(expo, (list, Variable)):
            new_expo = expo  
        elif isinstance(expo, Constant):
            new_expo = base.expo * expo.eval()
        return Variable(base.e, coeff = base.coeff, expo = new_expo)
    elif isinstance(base, Constant):
        if isinstance(expo, (list, Variable)):
            return Constant(base.eval(), expo = base.expo)
        elif isinstance(expo, Constant):
            return Constant(base.eval() ** expo.eval())
"""
def pow(base,expo):
    if isinstance(base, Variable):
        if isinstance(expo, (str,Variable)):
            return Variable(base.e, coeff = base.coeff, expo = expo)
        else:
            return Variable(base.e, coeff= base.coeff, expo= base.expo*expo)
    else:
        if isinstance(expo, (str,Variable)):
            #print(Variable(Empty(), coeff=base, expo = expo))

            return Variable(Empty(), coeff=base, expo = expo)
        else:
            return base**expo
        

def checkTerm(left,right):
    if isinstance(left,right.__class__):
        if isinstance(left, Constant):
            return True
        else:
            if left.e.symbol == right.e.symbol and left.expo == right.expo:
                return True
            else:
                return False
    else:
        return False

def calcByTerm(op, left,right):
    temp = []
    flag = False
    if isinstance(left, list):
        for idx, element in enumerate(left):
            if checkTerm(element,right):
                new_left = calc(op, element, right)
                temp.append(new_left)
                temp.extend(left[idx+1:])
                flag = True
                break
            temp.append(element)
        if not flag: temp.extend([op, right])
        
        return temp
    else:
        return calc(op, left, right)

def calc(op, left, right):
    if op is '+':
        return left + right
    elif op is '-':
        return left - right
    elif op is '*':
        return left * right
    elif op is '/':
        return left / right

def calcVariable(variable):
    return Constant(variable * pow(variable.e, variable.expo))
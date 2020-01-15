import math
from factor_new import Variable, Constant
from mathematical_constant import *

def logn(n, x = math.e):
    print(n/x)
    return 1 + logn(n/x, x) if n > (x-1) else 0

def lognNew(n, x = E):
    return math.log(n) / math.log(x)

def triangleFunction(func, expr):
    if func == 'sin':
        return math.sin(expr)
    elif func == 'cos':
        return math.cos(expr)
    elif func == 'tan':
        return math.tan(expr)

def pow(base,expo):
    if isinstance(base, Variable):
        print(base, expo)
        base.expo = base.expo * expo
        print(base.expo)
        return base
    elif isinstance(base, Constant):
        return base.e ** expo

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
    print(left, right)
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
import math
from factor_new import Variable, Constant, Symbol
from mathematical_constant import *
from empty import Empty
from copy import deepcopy

def logn(n, x = math.e):
    print(n/x)
    return 1 + logn(n/x, x) if n > (x-1) else 0

def lognNew(n, x = E):
    return math.log(n) / math.log(x)

def pow(base,expo):
    if isinstance(base, Variable):
        if isinstance(expo, (list,Variable)):
            return Variable(base.e, coeff = base.coeff, expo = expo)
        elif isinstance(base.e, Empty):
            return base.coeff**expo
        elif isinstance(base.e, float):
            return base.e**expo
        else:
            return Variable(base.e, coeff= base.coeff, expo= base.expo*expo)
    elif isinstance(base,list):
        if isinstance(expo, (int,float)):
            right = deepcopy(base)
            left = deepcopy(base)
            print(left)
            while (expo > 1):
                expo -= 1
                left = calcByTerm('*',left,right)
                print(left)
            return Variable(Empty(), coeff=left)
    else:
        if isinstance(expo, (list,Variable)):
            return Variable(Empty(), coeff=base, expo = expo)
        else:
            return base**expo
        
def isOperator(op):
    if op in ('+','-','/','*'):return True
    else: False

def checkTerm(left,right):
    if isinstance(left,right.__class__):
        if isinstance(left, float):
            return True
        else:
            if isinstance(left.e, Symbol):
                if left.e == right.e and left.expo == right.expo:
                        return True
            else:
                if left.e == right.e:
                    if left.expo == right.expo:
                        return True

    else:
        return False

def calcByTerm(op, left,right):
    temp = []
    no_same_term = True
    #print('step 1 = ', left, op, right)
    #if left == (x+1)
    try:
        if isinstance(left, list):
            #if right == (x+10)
            if isinstance(right, list):
                if op in ('+', '-'):
                    right_temp = []
                    for element in right:
                        if isOperator(element):
                            if op == '-':
                                if element == '+':
                                    element = '-'
                                else:
                                    element = '+'
                        right_temp.append(element)
                    right_temp.insert(0,op)
                    temp = left + right_temp
                    temp = clearExpr(temp)
                    return clearExpr(temp)
                else:

                    for left_idx in range(0, len(left), 2):
                        left_op, left_element = None, None
                        if left_idx == 0:
                            left_element = left[left_idx]
                        
                        else:
                            left_op = left[left_idx-1]
                            left_element = left[left_idx]
                        
                        if left_op == '-':
                            left_element = -left_element
                        
                        for right_idx in range(0,len(right),2):
                            right_op, right_element = None, None
                            if right_idx == 0:
                                right_element = right[right_idx]
                            else:
                                right_op = right[right_idx-1]
                                right_element = right[right_idx]
                            
                            if right_op == '-':
                                right_element = -right_element
                            res = calc(op,left_element,right_element)
                            res_list = ['+',res] if len(temp) > 0 else [res]
                            temp.extend(res_list)
                    temp = clearExpr(temp)      
                    return clearExpr(temp)
            else:
                if op in ('+', '-'):
                    temp = left[:]
                    temp.extend([op,right])
                    temp = clearExpr(temp)
                    return clearExpr(temp)
                # * /
                else:
                    for idx in range(0,len(left),2):
                        left_op, element = None, None
                        if idx == 0:
                            element = left[idx]
                            temp.append(calc(op,element,right))
                        else:
                            left_op = left[idx-1]
                            element = left[idx]
                            if left_op == '-':
                                element = -element
                            res = calc(op,element,right)
                            res_list = ['+',res]
                            temp.extend(res_list)                    
                    temp = clearExpr(temp)
                    return clearExpr(temp)
        else:
            return calc(op, left, right)
    except ZeroDivisionError:
        raise ZeroDivisionError

def calc(op, left, right):
    if op is '+':
        return left + right
    elif op is '-':
        return left - right
    elif op is '*':
        return left * right
    elif op is '/':
        return left / right

def clearExpr(left):
    res = 0
    variable_list = []
    if isinstance(left, (int, float, Variable)): return left
    for idx in range(0,len(left),2):
        
        if idx == 0:
            if isinstance(left[idx], (int,float)):
                res += left[idx]
            else:
                variable_list.append(left[idx])
        else:
            op = left[idx-1]
            element = left[idx]
            if isinstance(element,(int,float)):
                res = calc(op,res,element)
            else:
                if len(variable_list) == 0:
                    if op == '-':
                        element = -element
                    variable_list.append(element)

                else:
                    no_same_term = True
                    temp = []
                    for variable_idx in range(0,len(variable_list),2):
                        
                        if variable_idx == 0:
                            right_op = "+"
                            right = variable_list[variable_idx]
                        else:
                            right_op = variable_list[variable_idx-1]
                            right =  variable_list[variable_idx]
                        
                        if checkTerm(element,right):
                            if op == '-':
                                element = -element
                                op = '+'
                            if right_op == '-':
                                right = -right
                                right_op = '+'
                            variable_res = calc(op,element, right)
                            no_same_term = False
                            if variable_res == 0: 
                                temp.extend(variable_list[variable_idx+1:])
                                break
                            else:
                                res_list = ['+',variable_res] if len(temp) > 0 else [variable_res]
                                temp.extend(res_list)
                                temp.extend(variable_list[variable_idx+1:])
                                break
                        
                        temp.extend([right_op,right]) if variable_idx != 0 else temp.append(right)
                    
                    if no_same_term: temp.extend([op,element])
                    
                    variable_list = temp
    if len(variable_list) != 0:
        if res != 0:
            variable_list.extend(['+',res])
        return variable_list
    else:
        return res

def calcVariable(variable):
    return Constant(variable * pow(variable.e, variable.expo))

def isExpr(expr):
    sub_expr = expr.eval() 
    print(sub_expr, type(sub_expr), 'isExpr')
    if isinstance(sub_expr, list): return sub_expr.e
    return isExpr(sub_expr.e)

def checkDomain(expr):
    
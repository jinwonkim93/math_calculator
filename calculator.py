import math
from factor import Variable, Constant, Symbol, Parenthesis
from mathematical_constant import *
from empty import Empty
from copy import deepcopy

def logn(n, x = math.e):
    return 1 + logn(n/x, x) if n > (x-1) else 0

def pow(base,expo):
    if isinstance(base, Variable) and isinstance(base.e, Parenthesis):
        base = base.e.getList()
    if isinstance(base, Variable):
        if isinstance(expo, (list,Variable)):
            return Variable(base.e, coeff = base.coeff, expo = expo)
        elif isinstance(base.e, Empty) and isinstance(base.coeff, (int,float)):
            return base.coeff**expo
        elif isinstance(base.e, float):
            return base.e**expo
        elif abs(expo) < 1 and abs(expo) > 0:
            temp = Parenthesis([Variable(base.e, coeff= base.coeff, expo= base.expo)])
            return Variable(temp,expo = expo)
        else:
            return Variable(base.e, coeff= base.coeff, expo= base.expo*expo)
    
    elif isinstance(base,list):
        if isinstance(expo, (int,float)):
            right = deepcopy(base)
            left = deepcopy(base)
            if expo <1:
                print(base, type(base))
                return Variable(Parenthesis(base), expo = expo)
 
            while (expo > 1):
                expo -= 1
                left = calcByTerm('*',left,right)
            return left
        
        elif isinstance(expo, (list,Variable)):
            return Variable(Empty(), coeff=base, expo = expo)
    else:
        if isinstance(expo, Variable):
            return Variable(Empty(),coeff = base, expo = expo)
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
                    if type(left.coeff) == type(right.coeff):
                        return True
            else:
                if left.e == right.e:
                    if left.expo == right.expo:
                        return True

    else:
        return False

def checkTerm2(myExpr,other):
    if isinstance(myExpr, Variable) and isinstance(other, Variable):
        if myExpr.e == other.e and myExpr.expo == other.expo:
            if isinstance(myExpr.coeff, (int,float)) and isinstance(other.coeff, (int,float)):
                return True
            elif isinstance(myExpr.coeff, Variable) and isinstance(other.coeff, Variable):
                    return checkTerm2(myExpr.coeff, other.coeff)
            else:
                return False
        return False
    elif isinstance(myExpr, (int,float)) and isinstance(other, (int, float)):
        return True
    else:
        return False
    
def list2str(expr):
    try:
        d = ''
        for element in expr:
            if isinstance(element, list):
                element = list2str(element)
            d += str(element)
        return d
    except:
        return str(expr)

def calcByTerm(op, left,right):
    temp = []
    no_same_term = True

    
    if isinstance(left, Variable) and isinstance(left.e, Parenthesis):
        if left.expo == 1:
            temp_left = clearExpr(left.e.getList())
            temp_left = clearExpr(temp_left)
            left = calcByTerm('*', temp_left, left.coeff)
            left = left.e.getList() if isinstance(left, Variable) else left
        elif left.expo > 1:
            temp_left = left.e.getList()
            temp_left = pow(temp_left, left.expo)
            left = calcByTerm('*',temp_left,left.coeff)
            left = left.e.getList() if isinstance(left, Variable) else left
            # left = left.e.getList()
    
    if isinstance(right, Variable) and isinstance(right.e, Parenthesis):
        if right.expo == 1:
            temp_right = clearExpr(right.e.getList())
            temp_right = clearExpr(temp_right)
            right = calcByTerm('*', temp_right,right.coeff) 
            right = right.e.getList()
        elif right.expo > 1:
            temp_right = right.e.getList()
            temp_right = pow(temp_right, right.expo)
            right = calcByTerm('*',temp_right,right.coeff)
            right = right.e.getList()
            
    
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
                    if op == '/':
                        left = Variable(Parenthesis(left))
                        right = Variable(Parenthesis(right))
                        res = calc(op,left,right)
                        return res
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
                        res = Variable(Parenthesis(temp))  
                        return res
            elif isinstance(right, (float,Variable)):
                if op in ('+', '-'):
                    temp.extend(left)
                    if op is '-':
                        right = -right
                        temp.extend(['+',right])
                    else:
                        temp.extend([op,right])
                    temp = clearExpr(temp)
                    res = Variable(Parenthesis(temp))
                    return res
                # * /
                else:
                    for idx in range(0,len(left),2):
                        left_op, element = None, None
                        if idx == 0:
                            element = left[idx]
                            res = calcByTerm(op,element,right)
                            temp.append(res)
                        else:
                            left_op = left[idx-1]
                            element = left[idx]
                            if left_op == '-':
                                element = -element
                                res = calcByTerm(op,element,right)
                                res_list = ['+',res]
                            else:
                                res = calcByTerm(op,element,right)
                                res_list = [left_op,res]
                            temp.extend(res_list)
                    temp = clearExpr(temp)
                    res = Variable(Parenthesis(temp))
                    return res
        elif isinstance(left, (float, Variable)):
            if isinstance(right, list):
                right = clearExpr(right)
                if op in ('+', '-'):
                    temp.append(left)
                    temp.append(op)
                    for idx in range(0,len(right),2):    
                        
                        if idx == 0:
                            right_element = right[idx]
                            if op is '-':
                                right_element = -right_element
                            temp.append(right_element)
                        else:
                            right_op = right[idx-1]
                            right_element = right[idx]

                            if op is '-':
                                if op == right_op:
                                    right_op = '+'
                                else:
                                    right_op = '-'
                            temp.extend([right_op,right_element])
                    temp = clearExpr(temp)
                    return clearExpr(temp)
                # * /
                else:
                    if op =='*':
                        for idx in range(0,len(right),2):
                            left_op, element = None, None
                            if idx == 0:
                                element = right[idx]
                                temp.append(calc(op,left,element))
                            else:
                                right_op = right[idx-1]
                                element = right[idx]
                                if right_op == '-':
                                    element = -element
                                    res = calc(op,left,element)
                                else:
                                    res = calc(op,left,element)
                                    res_list = [right_op,res]
                                temp.extend(res_list)
                        temp = clearExpr(temp)
                        return temp
                    else:
                        right = Variable(Parenthesis(right))
                        res = calc(op,left,right)
                        return res
            
            elif isinstance(right, (float,Variable)):
                result = calc(op, left, right)
                return clearExpr(result)
        else:
            result = calc(op, left, right)
            return result
    
    except ZeroDivisionError:
        raise ZeroDivisionError
    except Exception as e:
        raise e

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
                        if checkTerm2(element,right):
                            if op == '-':
                                element = -element
                                op = '+'
                            if right_op == '-':
                                right = -right
                                right_op = '+'
                            variable_res = calc(op,element, right)
                            no_same_term = False
                            if variable_res == 0:
                                if variable_idx == 0:
                                    variable_list.pop(0)
                                temp.extend(variable_list[variable_idx+1:])
                                break
                            else:
                                res_list = ['+',variable_res] if len(temp) > 0 else [variable_res]
                                temp.extend(res_list)
                                temp.extend(variable_list[variable_idx+1:])
                                break
                        temp.extend([right_op,right]) if variable_idx != 0 else temp.append(right)

                    if no_same_term: temp.extend([op,element])
                    
                    variable_list = deepcopy(temp)
    
    if len(variable_list) != 0:
        varaiable_list = sortVariable(variable_list)
        if res != 0:
            variable_list.extend(['+',res])
        
        return variable_list
    else:
        return [res]

def sortVariable(expr):
    if not isinstance(expr, list): return expr
    if expr[0] != '-':
        expr.insert(0,'+')
    for idx in range(1,len(expr),2):
        for jdx in range(1, len(expr)-idx, 2):
            if isinstance(expr[jdx], Variable) and isinstance(expr[jdx+2], Variable):
                if expr[jdx].e > expr[jdx+2].e:
                    expr[jdx-1], expr[jdx], expr[jdx+1], expr[jdx+2] =  expr[jdx+1], expr[jdx+2], expr[jdx-1], expr[jdx]
                elif expr[jdx].e == expr[jdx+2].e:
                    if expr[jdx].expo < expr[jdx+2].expo:
                        expr[jdx-1], expr[jdx], expr[jdx+1], expr[jdx+2] =  expr[jdx+1], expr[jdx+2], expr[jdx-1], expr[jdx]

    if expr[0] != '-':
        expr.pop(0)
    return expr        

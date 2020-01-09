import re

#infix to postfix

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def pref(x):
    if x == '*' or x == '/':
        return 1
    elif x == '+' or x == '-':
        return 0
    elif x == '(':
        return -1

def postfix_operator_work(element: str, stack: list, postfix: list):
        pivot = pref(element)
        while len(stack) > 0:
            top = stack[-1]
            if pref(top) <= pivot: break
            postfix.append(stack.pop())
        stack.append(element)

def convert_expression(expression: str) -> list:
    #[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)? match numbers with exponents
    #return [ e for e in re.split(r'(\D)', expression) if e not in ('', ' ')]
    return re.findall('[-+]?[0-9]*\.?[0-9]+|[*+-/()]', expression)
    
def infix2postfix(expression: str) -> list:
    postfix = []
    stack = []
    expression = convert_expression(expression)
    negative_flag = False
    #bracket_flag = []
    try:
        for idx, element in enumerate(expression):
            if element in ('*','/','+','-'):
                if element == '-':
                    if expression[idx-1] in ('*','/','+','-','(') or idx == 0:
                        negative_flag = ~negative_flag
                        continue
                postfix_operator_work(element,stack,postfix)

            elif element =='(':
                #bracket_flag.append(True)
                stack.append(element)
            
            elif element == ')':
                #bracket_flag.pop()
                while True:
                    now = stack.pop()
                    if now == '(':
                        break
                    postfix.append(now)
            
            elif element.isnumeric() or isfloat(element):
                if negative_flag:
                    postfix.append(-float(element))
                    #if not any(bracket_flag):
                    negative_flag = ~negative_flag
                else:
                    postfix.append(float(element))
        
        if len(stack) > 0:
            while len(stack) > 0:
                now = stack.pop()
                postfix.append(now)
        return postfix

    except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름을 받아오는 변수
        



def calc_postfix(expression: list) -> float:
    stack = []
    try:
        for element in expression:
            if element in ('*','/','+','-'):
                op1, op2, result = stack.pop(), stack.pop(), 0
                
                try:
                    if element == "*":
                        result = op2 * op1
                    elif element == '/':
                        result = op2 / op1
                    elif element == '+':
                        result = op2 + op1
                    elif element =='-':
                        result = op2 - op1
                    stack.append(result)
                except ZeroDivisionError as e: # 에러 종류
                    raise ZeroDivisionError(e) # ex는 발생한 에러의 이름을 받아오는 변수
            else:
                stack.append(element)
        if len(stack) != 1:
            raise ValueError("invalid expression, operators and operands don't match")
    
    except (ValueError, IndexError, ZeroDivisionError, TypeError) as e:
        return e
            
    else:  
        return stack.pop()

def run_calc(expression: str) -> [str, list]:
    postfix = infix2postfix(expression)
    return calc_postfix(postfix), postfix

import re

#infix to postfix
class Stack_calculator(object):
    def __init__(self):
        self.postfix = []

    def is_unary(self, element: str, element_before: str):
        if element == '-' or element == '+':
            if element_before in ('*','/','+','-','('):
                return True
        return False

    def is_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get_priority(self, operator: str) -> int:
        if operator == '*' or operator == '/':
            return 1
        elif operator == '+' or operator == '-':
            return 0
        elif operator == '(':
            return -1

    def postfix_operator_work(self, operator: str, stack: list):
            pivot = self.get_priority(operator)
            while len(stack) > 0:
                top = stack[-1]
                if self.get_priority(top) < pivot: break
                self.postfix.append(stack.pop())
            stack.append(operator)

    def convert_expression(self, expression: str) -> list:
        #[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)? match numbers with exponents
        #return [ e for e in re.split(r'(\D)', expression) if e not in ('', ' ')]
        return re.findall(r'[-+]|[0-9]*\.?[0-9]+|[*+-/()]', expression)
        
    def convert_infix2postfix(self, expression: str) -> list:
        stack = []
        expression = self.convert_expression(expression)
        negative_flag = False
        #bracket_flag = []1
        try:
            for idx, element in enumerate(expression):
                if element in ('*','/','+','-'):
                    if idx == 0 or self.is_unary(element,expression[idx-1]):
                        if element == '-':
                            negative_flag = ~negative_flag
                        continue
                    self.postfix_operator_work(element,stack)

                elif element =='(':
                    #bracket_flag.append(True)
                    stack.append(element)
                
                elif element == ')':
                    #bracket_flag.pop()
                    while True:
                        now = stack.pop()
                        if now == '(':
                            break
                        self.postfix.append(now)
                
                elif element.isnumeric() or self.is_float(element):
                    if negative_flag:
                        self.postfix.append(-float(element))
                        #if not any(bracket_flag):
                        negative_flag = ~negative_flag
                    else:
                        self.postfix.append(float(element))
            
            if len(stack) > 0:
                while len(stack) > 0:
                    now = stack.pop()
                    self.postfix.append(now)
            return self.postfix

        except Exception as ex: # 에러 종류
                print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름을 받아오는 변수
            



    def calc_postfix(self, expression: list) -> float:
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
    calc = Stack_calculator()
    postfix = calc.convert_infix2postfix(expression)
    #assert 8 == calc.calc_postfix(postfix)

    return calc.calc_postfix(postfix), postfix

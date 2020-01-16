
class Node(object):
    def __init__(self, op):
        self.op = op


    def calc(self, left, right):
        if self.op is '+':
            return left + right
        elif self.op is '-':
            return left - right
        elif self.op is '*':
            return left * right
        elif self.op is '/':
            return left / right
    
    """        
    def calcByTerm(self, left,right, checkTerm):
        print(left, right)
        temp = []
        flag = False
        if isinstance(left, list):
            for idx, element in enumerate(left):
                print(element)
                if checkTerm(element,right):
                    new_left = self.calc(element, right)
                    temp.append(new_left) 
                    temp.extend(left[idx+1:])
                    flag = True
                    break
                temp.append(element)
            if not flag: temp.extend([self.op, right])
            return temp
        else:
            return self.calc(left, right)

    """


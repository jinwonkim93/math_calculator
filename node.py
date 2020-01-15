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
    
        
    def calcByTerm(self, left,right, checkTerm):
        print(left, right)
        if isinstance(left, list):
            for idx, element in enumerate(left):
                if checkTerm(element,right):
                    new_ = self.calc(element, right)
                    temp.append(left)
                    temp.extend(left[idx+1:])
                    break
                else:
                    temp.append(element)
        else:
            return self.calc(left, right)

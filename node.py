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
    
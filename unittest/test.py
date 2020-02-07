import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.getcwd())
from calculator.parser import Parser
from calculator.scanner import Scanner

line = '5+5+-5+5+4+-3+1'
token = Scanner(line)
parser = Parser(token)
tree = parser.parse()
print(tree)
print(repr(tree))
a = tree.canonicalize()
print(a)
print(repr(a))
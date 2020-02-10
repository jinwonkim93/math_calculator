import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.getcwd())
from calculator.parser import Parser
from calculator.scanner import Scanner
testCase = ['1+1+1',
'x+1',
'5+x-1',
'2*2 + 5',
'x+y',
'y+x',
'x-x-x']

def test(line):
    token = Scanner(line)
    parser = Parser(token)
    tree = parser.parse()
    print(tree)
    print(repr(tree))
    a = tree.canonicalize()
    # a = a.canonicalize()
    print(a)
    print(repr(a))

# for idx,case in enumerate(testCase):
#     print(f'-------test case {idx}--------')
#     try:
#         test(case)
#     except Exception as e:
#         print('Error = ', e)

line = '2*x'
test(line)
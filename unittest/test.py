import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.getcwd())
from calculator.parser import Parser
from calculator.scanner import Scanner
# testCase = ['1+5',
# '5-5',
# 'x+y+x+sin(x)',
# 'x/x*5+x/x',
# 'log(x)',
# 'log(2,x)',
# '(x+5+5)+5']
testCase = ['x*2',
'(5-5)',
'(x+y)+(x+sin(x))',
'((x/x*5)+x/x)',
'log(x)',
'log(2,x)',
'(x+5+5)+5',
'2*x',
'x*2',
'2*x*y-3',
'x+y+1',
'5+x+x^2+x^3+2^x',
'2^x+2^x',
'(x+2)*2']


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

line = '(x+1)*x^-1'
test(line)
# line = '1*x'
# test(line)
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
testCase = [
    'x+x',
    'x*y',
    '2*x*y',
    'x*x + 2*x',
    'x*x*x*x/x*y*y*x'
            ]


def test(line):
    token = Scanner(line)
    parser = Parser(token)
    tree = parser.parse()
    print('')
    print(tree)
    print('')
    print(repr(tree))
    print('')
    a = tree.canonicalize()
    print(a)
    print('')
    print(repr(a))
    print('')
    print('calc',a.eval({'x':1,'y':1}))
    print(a.getVariables())
    del a
    # derivatives = a.getDerivative('x')
    # print(derivatives, type(derivatives), repr(derivatives))

# for idx,case in enumerate(testCase):
#     print(f'-------test case {idx}--------')
#     test(case)
#     # try:
#     #     test(case)
#     # except Exception as e:
#     #     print('Error = ', e)

# line = 'x+(x+2)'
# line = 'x*y + 2*x'
line = 'x*x*x*x/x*y*y*x'
test(line)
# line = '1*x'
# test(line)

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.getcwd())
from calculator.parser import Parser
from calculator.scanner import Scanner
testCase = ['1+5',
'5-5',
'x+y+x+sin(x)',
'x/x*5+x/x',
'log(x)',
'log(2,x)',
'(x+5+5)+5']
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
'(x+2)*2',
'(x+1)/(x+1)']


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
    b = tree.canonicalize()
    # a = a.canonicalize()
    # a = a.canonicalize()
    a.insertTerm(b.term)
    b.term.coefficient = 3
    print(a)
    print(b)
    print(len(a))
    print('')
    print(repr(a))
    print('')
    a.insertValue({'x':1,'y':1})
    print('calc',a.eval())

    # derivatives = a.getDerivative('x')
    # print(derivatives, type(derivatives), repr(derivatives))

# for idx,case in enumerate(testCase):
#     print(f'-------test case {idx}--------')
#     try:
#         test(case)
#     except Exception as e:
#         print('Error = ', e)

line = 'x+x+5+x^2'
# line = 'x*y + 2*x'
# line = '2*x+x*y'
test(line)
# line = '1*x'
# test(line)

from scanner import Scanner
from parser import Parser

def test(case):

    print('-'*50)
    scanner = Scanner(case)    
    parser = Parser(scanner)
    print(scanner.tokens)
    tree = parser.parse()
    print(parser.variables)
    parser.insertValue()
    print(tree.eval())
    print(tree.getCalc())
    print(parser.getDerivative(tree))
    #print(repr(tree))
    #print(tree)
    print('-'*50)


"""with open('../parser/test_case.txt','r') as question:
    for ql in question:
        test(ql)"""

with open('tri.txt','r') as question:
    for ql in question:
        test(ql)


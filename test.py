from function_calculator import *

def test(case):
    print('-'*50)
    scanner = Scanner(case)    
    parser = Parser(scanner)
    print(scanner.tokens)
    tree = parser.parse()
    print(parser.variables)
    parser.insertValue()
    print(tree.eval())
    print(repr(tree))
    print(tree)
    print('-'*50)

with open('../parser/test_case.txt','r') as question:
    for ql, al in question:
        test(ql)

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
    print(parser.domain)
    print('-'*50)


test(input())
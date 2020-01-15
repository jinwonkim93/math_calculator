from scanner import Scanner
from parser import Parser

def test(case):
    try:
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
    except Exception as e:
        print(e)

test(input())
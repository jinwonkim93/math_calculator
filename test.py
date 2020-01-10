def test(test_cases):
    for case in test_cases:
        print('-'*50)
        scanner = Scanner(case)    
        parser = Parser(scanner)
        print(scanner.tokens)
        tree = parser.parse()
        print(parser.variables)
        parser.insertValue()
        print('answer is ',tree.eval())
        print(repr(tree))
        print(tree)
        print('-'*50)

with open('../parser/test_case.txt',r) as f:
    for l in f:
        test(l)

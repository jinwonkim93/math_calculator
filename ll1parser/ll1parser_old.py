PLUS = '+'
MINUS = '-'
MULTI = '*'
DIVI = '/'
PAR_OPEN = '('
PAR_CLOSE = ')'

import re


class Tokenizer(object):
    def __init__(self, expression = None):
        self._expression = expression
        self._tokens = re.findall(r'[-+]|[0-9]*\.?[0-9]+|[*+-/()]', self._expression)
        
    def nextSym(self) -> str:
        for sym in self._tokens:
            yield sym
            

def isDigit(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

    
def parseExpr(tree, nextSym):
    #subTree = ['Expr']
    #print('parseExpr')
    tree.append('Expr')
    if not parseTerm(tree, nextSym): return False
    print('T finish')
    if not parseExprTail(tree, nextSym): return False
    print('E_t finish')
    #tree.append(subTree)
    return True


def parseExprTail(tree, nextSym):
    subTree = ['ExprTail']
    if len(nextSym) == 0: return True
    lookUp = nextSym[0]
    if lookUp is PAR_CLOSE:
        nextSym.pop(0)
        return True
    #print("parseExprTail")
    if lookUp not in [PLUS,MINUS]: return True

    if lookUp is PLUS:
        subTree.append([nextSym.pop(0)])
    elif lookUp is MINUS:
        subTree.append([nextSym.pop(0)])

    if not parseTerm(subTree, nextSym): return False
    if not parseExprTail(subTree, nextSym): return False

    tree.append(subTree)
     
    return True

    
def parseTerm(tree, nextSym):
    subTree = ['Term']
    #print('parseTerm')
    if not parseFactor(subTree, nextSym): return False
    if not parseTermTail(subTree, nextSym): return False
    tree.append(subTree)
    return True


def parseTermTail(tree, nextSym):
    subTree = ['TermTail']
    #print('parseTermTail')
    if len(nextSym) == 0: return True
    lookUp = nextSym[0]
    if lookUp is PAR_CLOSE:
        nextSym.pop(0)
        return True
        
    if lookUp not in [MULTI, DIVI]: return True
    
    if lookUp is MULTI:
        subTree.append([nextSym.pop(0)])
    elif lookUp is DIVI:
        subTree.append([nextSym.pop(0)])

    if not parseFactor(subTree, nextSym): return False
    if not parseTermTail(subTree, nextSym): return False
    
    tree.append(subTree)
    
    return True

def parseFactor(tree, nextSym):
    subTree = ['Factor']
    #print('parseFactor')
    lookUp = nextSym[0]
    if lookUp in [PLUS, MINUS]:
        if lookUp is PLUS:
            nextSym.pop(0)
            if not parseFactor(subTree, nextSym): return False
        if lookUp is MINUS:
            tmp = nextSym.pop(0)
            nextSym[0] = tmp+nextSym[0]
            if not parseFactor(subTree, nextSym): return False
    else:
        if not parsePrimaryExpr(subTree, nextSym): return False
    
    tree.append(subTree)
    return True

def parsePrimaryExpr(tree, nextSym):
    subTree = []
    lookUp = nextSym[0]

    if isDigit(lookUp):
        print('digit')
        subTree.append(float(nextSym.pop(0)))
        tree.append(subTree)
        return True
    
    if lookUp is PAR_OPEN:
        nextSym.pop(0)
        print('par_open')
        if not parseExpr(subTree, nextSym): return False
        tree.append(subTree)
        return True
    
def main():
    expr = input()
    tokens = Tokenizer(expr)
    nextSym = tokens._tokens
    tree = []
    parseExpr(tree, nextSym)
    print(tree)


main()
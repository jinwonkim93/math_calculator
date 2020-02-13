
def list2str(expr):
    try:
        d = ''
        for element in expr:
            if isinstance(element, list):
                element = list2str(element)
            d += str(element)
        return d
    except:
        return str(expr)

def sortVariable(expr):
    if not isinstance(expr, list): return expr
    if expr[0] != '-':
        expr.insert(0,'+')
    for idx in range(1,len(expr),2):
        for jdx in range(1, len(expr)-idx, 2):
            if jdx+2 >= len(expr): continue
            if not isinstance(expr[jdx], float) and not isinstance(expr[jdx+2], float):
                if expr[jdx].e > expr[jdx+2].e:
                    expr[jdx-1], expr[jdx], expr[jdx+1], expr[jdx+2] =  expr[jdx+1], expr[jdx+2], expr[jdx-1], expr[jdx]
                elif expr[jdx].e == expr[jdx+2].e:
                    if isinstance(expr[jdx].expo, float) and expr[jdx].expo < expr[jdx+2].expo:
                        expr[jdx-1], expr[jdx], expr[jdx+1], expr[jdx+2] =  expr[jdx+1], expr[jdx+2], expr[jdx-1], expr[jdx]

    if expr[0] != '-':
        expr.pop(0)
    return expr

def calc(op, left, right):
    if op is '+':
        return left + right
    elif op is '-':
        return left - right
    elif op is '*':
        return left * right
    elif op is '/':
        return left / right


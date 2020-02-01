from scanner import Scanner
from parser import Parser
import matplotlib.pyplot as plt, mpld3
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import io
import base64
from error import NonDerivableError, Error
from utils import clearExpr
mpl.use('Agg')

domainRule = {
    "!=":lambda x,y: x != y
}
#사용안함
def checkDomain(parser,tree, value):
    domain = parser.getDomain()
    parser.insertValue(value)
    validity = True
    print(domain)
    for symbol, rule in domain:
        rule_op, invalid_value = rule.split(',')
        try:
            test_value = symbol.getCalc()
        except:
            return False
        validity &= domainRule[rule_op](test_value, float(invalid_value))
    return validity

def isContinuous(parser,tree, value):
    # if checkDomain(parser,tree, value) == False:
        # return False
    alpha = 10**-5
    tolerance = alpha * 10000
    try:
        parser.insertValue(value)
        mid = tree.getCalc()
    except:
        return False 
    parser.insertValue(value-alpha)
    left = tree.getCalc()
    parser.insertValue(value+alpha)
    right = tree.getCalc()
    #print('mid', mid, type(mid))
    #print('left', left, type(left))
    #print('right', right, type(right))
    #print( abs(left-mid)<tolerance and abs(mid-right)<tolerance)
    return abs(left-mid)<tolerance and abs(mid-right)<tolerance

def isDerivative(parser, tree, value):
    result = False
    if isContinuous(parser, tree, value):
        derivatives = parser.getDerivative(tree)
        if derivatives is not None:
            for d in derivatives:
                semi_expr = str(d[1])
                d_parser = getParser(semi_expr)
                d_tree = d_parser.parse()
                d_parser.insertValue(value)
                try:
                    val = d_tree.getCalc()
                    result = True
                except:
                    result = False
    return result


def plot2D(parser, tree, start, end):
    values = np.linspace(start, end , 1000)
    x = []
    y = []

    for value in values:
        if isContinuous(parser,tree, value):
            parser.insertValue(value)
            mid = tree.getCalc()     
            x.append(value)
            y.append(mid)
        else:
            x.append(np.nan)
            y.append(np.nan)
                   

    x = np.asarray(x)
    y = np.asarray(y)
    return [x,y]

def plot3D(parser, tree, start, end):
    #x = np.arange(start,end, 0.1)
    x = np.linspace(start, end, 200)
    y = []
    for value1 in x:
        parser.insertValue2(value1,'x')

        temp = []
        for value2 in x:
            parser.insertValue2(value2,'y')
            ans = tree.getCalc()
            #print(ans)
            temp.append(ans)
        y.append(temp)
    y = np.asarray(y)
    return [x,x,y]

def draw2D(data, figure_num, title):
    x,y = data
    fig = plt.figure(figure_num)
    ax = plt.axes()
    ax.set_xlabel('x')
    ax.set_ylabel('y',rotation=0)
    vmin = np.nanmin(y); vmax = np.nanmax(y)
    #print(y)
    plt.ylim(vmin, vmax)
    plt.title(title)
    plt.plot(x,y)
    plt.close()
    return mpld3.fig_to_html(fig,template_type ='simple')

def drawMulti(data, figure_num, title):
    mpl.rcParams['legend.fontsize'] = 10
    x,y,z = data
    fig = plt.figure(figure_num)
    ax = plt.axes(projection='3d')
    plt.title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.contour3D(x, y, z, 50)
    vmin = np.nanmin(y); vmax = np.nanmax(y)
    #print(y)
    plt.ylim(vmin, vmax)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)
        
def list2str(expr):
    try:
        d = ''
        for element in expr:
            #print(element, type(element))
            if isinstance(element, list):
                element = list2str(element)
            d += str(element)
        return d
    except Exception as e:
        return str(expr)
        #return expr

def getParser(case):
    scanner = Scanner(case)
    print('tokenized = ', scanner.tokens)  
    parser = Parser(scanner)
    return parser

def test2(case, start_end):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    if isinstance(tree, Error):
        return [], tree, [], []
    canonicalization = tree.eval()
    print(type(canonicalization))
    canonicalization = list2str(canonicalization)
    print('tree = ',tree)
    print('canonicalization = ',canonicalization)
    variable_num = len(parser.getVariables())
    start, end = start_end
    figure_num = 1
    domain = parser.getDomain()

    if not isinstance(canonicalization, (int,float)):
        if variable_num > 1:
            data = plot3D(parser, tree, start, end)
            pics.append(drawMulti(data, figure_num, canonicalization))  
        elif variable_num == 1:
            data = plot2D(parser, tree, start, end)
            pics.append(draw2D(data, figure_num, canonicalization))    
        print(isDerivative(parser,tree,-1))
    derivatives = parser.getDerivative(tree)
    domain = list(parser.getDomain())
    print('derivatives =', derivatives)
    if derivatives is None:
        derivatives = []
    print('domain =', domain)
    if derivatives is not None:
        for d in derivatives:
            # print(d, type(d))
            d[1] = list2str(d[1])
            figure_num += 1
            semi_expr = list2str(d[1])
            partial_derivatives.append(list2str(d))
            d_parser = getParser(semi_expr)
            d_tree = d_parser.parse()
            d_title = semi_expr
            if len(d_parser.getVariables()) == 0: continue
            d_data = plot2D(d_parser, d_tree, start, end)
            pics.append(draw2D(d_data, figure_num, d_title))
    
    return pics, canonicalization, derivatives, domain
    # return pics, canonicalization, partial_derivatives, domain

def test(case, start_end):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    if isinstance(tree, Error):
        return [], tree, [], []
    canonicalization = tree.eval()
    print(type(canonicalization))
    canonicalization = list2str(canonicalization)
    print('tree = ',tree)
    print('canonicalization = ',canonicalization)
    variable_num = len(parser.getVariables())
    start, end = start_end
    figure_num = 1
    # domain = parser.getDomain()

    if not isinstance(canonicalization, (int,float)):
        if variable_num > 1:
            data = plot3D(parser, tree, start, end)
            pics.append(drawMulti(data, figure_num, canonicalization))  
        elif variable_num == 1:
            data = plot2D(parser, tree, start, end)
            pics.append(draw2D(data, figure_num, canonicalization))    
        print(isDerivative(parser,tree,-1))
    derivatives = parser.getDerivative(tree)
    domain = list(parser.getDomain())
    print('derivatives =', derivatives)
    if derivatives is None:
        derivatives = []
    print('domain =', domain)
    if derivatives is not None:
        for d in derivatives:
            # print(d, type(d))
            d[1] = list2str(d[1])
            figure_num += 1
            semi_expr = list2str(d[1])
            partial_derivatives.append(list2str(d))
            d_parser = getParser(semi_expr)
            d_tree = d_parser.parse()
            d_title = semi_expr
            if len(d_parser.getVariables()) == 0: continue
            d_data = plot2D(d_parser, d_tree, start, end)
            pics.append(draw2D(d_data, figure_num, d_title))
    clean_domain = []
    for d in domain:
        clean_domain.append(list2str(d))

    # return pics, canonicalization, derivatives, domain
    return pics, canonicalization, partial_derivatives, clean_domain



#test2(input(),[-1,1])


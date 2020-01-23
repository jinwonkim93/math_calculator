from scanner import Scanner
from parser import Parser
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def draw2D(parser, tree, start,end, figure_num):
    x = np.arange(start,end, 0.1)
    y = []
    for value in x:
        parser.insertValue(value)
        ans = tree.getCalc()
        y.append(ans)
    plt.figure(figure_num)
    title = tree.eval()
    plt.title(title)
    plt.plot(x,y)
    plt.savefig(f'./static/{title}2d.png')
    plt.close()
    return f'{title}2d.png'

def drawMulti(parser, tree, start, end, figure_num):
    mpl.rcParams['legend.fontsize'] = 10			# 그냥 오른쪽 위에 뜨는 글자크기 설정이다.

    fig = plt.figure(figure_num)
    ax = plt.gca(projection='3d')
    title = tree.eval()
    plt.title(title)
    x = np.arange(start,end, 0.1)
    y = []
    
    for value1 in x:
        parser.insertValue2(value1,'x')
        temp = []
        for value2 in x:
            parser.insertValue2(value2,'y')
            ans = tree.getCalc()
            temp.append(ans)
        y.append(temp)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.contour3D(x, x, y, 50, label='parametric curve')
    # vmin = np.nanmin(y), vmax = np.nanmax(y)
    plt.savefig(f'./static/{title}3d.png')
    plt.close()
    return f'{title}3d.png'
    
def list2str(list):
    try:
        d = ''
        for element in list:
            d += str(element)
        return d
    except:
        return list

def getTree(case):
    scanner = Scanner(case)    
    print(scanner.tokens)
    parser = Parser(scanner)
    return parser

def test2(case):
    parser = getTree(case)
    tree = parser.parse()
    canonicalization = tree.eval()
    print(canonicalization)
    derivatives = parser.getDerivative(tree)
    print(derivatives)

def test(case):
    pics = []
    partial_derivatives = []
    parser = getTree(case)
    tree = parser.parse()
    canonicalization = tree.eval()
    variable_num = len(parser.variables)
    start = -1
    end = 1
    figure_num = 1
    
    if variable_num > 1:
        pics.append(drawMulti(parser,tree, start, end, figure_num))  
    elif variable_num == 1:
        pics.append(draw2D(parser,tree, start, end, figure_num))    
    derivatives = parser.getDerivative(tree)
    domain = parser.domain
    if derivatives is not None:
        for d in derivatives:
            partial_derivatives.append(list2str(d))
            #partial_derivatives.append(d)
            figure_num += 1
            semi_expr = str(d[1])
            d_parser = getTree(semi_expr)
            d_tree = d_parser.parse()
            if len(d_parser.variables) == 0: break
            pics.append(draw2D(d_parser,d_tree, start, end, figure_num))    

    return pics, list2str(canonicalization), partial_derivatives, domain
    #return pics, canonicalization, derivatives, domain





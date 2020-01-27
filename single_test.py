from scanner import Scanner
from parser import Parser
import matplotlib.pyplot as plt, mpld3
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import io
import base64
mpl.use('Agg')

#def isContinuous(parser,tree)
def plot2D(parser, tree, start, end):
    values = np.linspace(start * np.pi, end * np.pi, 1000)
    x = []
    y = []
    domain = parser.getDomain()
    #print('plot start')
    #print(domain)
    alpha = float(0.00000001)
    tolerance = float(0.0000001)
    
    for value in values:
        result=True
        parser.insertValue(value)
        mid = tree.getCalc()        
        parser.insertValue(value-alpha)
        left = tree.getCalc()
        parser.insertValue(value+alpha)
        right = tree.getCalc()
        print('left-mid ',abs(left-mid), abs(left-mid)<tolerance)
        print('mid-right ', abs(mid-right), abs(mid-right)<tolerance)
        if abs(left-mid)<tolerance and abs(mid-right)<tolerance:
            x.append(value)
            y.append(mid)
        else:
            x.append(np.nan)
            y.append(np.nan)
        #if domain:
            #if mid > 10: ans = np.nan
            #elif mid < -10: ans = np.nan
        #print(ans)

    x = np.asarray(x)
    y = np.asarray(y)
    return [x,y]

def plot3D(parser, tree, start, end):
    #x = np.arange(start,end, 0.1)
    x = np.linspace(start * np.pi, end * np.pi, 300)
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
    plt.ylim(vmin, vmax)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)
        
def list2str(list):
    try:
        d = ''
        for element in list:
            d += str(element)
        return d
    except:
        return list

def getParser(case):
    scanner = Scanner(case)    
    parser = Parser(scanner)
    return parser

def test2(case):
    parser = getTree(case)
    tree = parser.parse()
    canonicalization = tree.eval()
    print(canonicalization)
    derivatives = parser.getDerivative(tree)
    print(derivatives)

def test(case, start_end):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    canonicalization = list2str(tree.eval())
    variable_num = len(parser.getVariables())
    start, end = start_end
    figure_num = 1
    
    if variable_num > 1:
        data = plot3D(parser, tree, start, end)
        pics.append(drawMulti(data, figure_num, canonicalization))  
    elif variable_num == 1:
        data = plot2D(parser, tree, start, end)
        pics.append(draw2D(data, figure_num, canonicalization))    
    
    derivatives = parser.getDerivative(tree)
    domain = parser.getDomain()
    
    if derivatives is not None:
        for d in derivatives:
            partial_derivatives.append(list2str(d))
            figure_num += 1
            semi_expr = str(d[1])
            print(d)
            d_parser = getParser(semi_expr)
            d_tree = d_parser.parse()
            d_title = d_tree.eval()
            d_data = plot2D(d_parser, d_tree, start, end)
            if len(d_parser.getVariables()) == 0: break
            pics.append(draw2D(d_data, figure_num, d_title))    

    return pics, canonicalization, partial_derivatives, domain







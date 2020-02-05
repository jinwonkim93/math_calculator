from scanner import Scanner
from parser import Parser
import matplotlib.pyplot as plt, mpld3
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import io
import base64
from error import NonDerivableError, Error
from calculator import clearExpr, getDerivative
from utils import list2str
mpl.use('Agg')
from copy import deepcopy

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
            test_value = symbol.eval()
        except:
            return False
        validity &= domainRule[rule_op](test_value, float(invalid_value))
    return validity

def derivativeAtPoint(parser,tree,value, derivatives):
    value_dict = {}
    for element in value:
        symbol, point = element.split('=')
        value_dict[symbol] = float(point)
    result = False
    if isContinuous(parser,tree, value_dict):
        if derivatives == None or len(derivatives) == 0: return True
        for d in derivatives:
            d[1] = list2str(d[1])
            semi_expr = list2str(d[1])
            d_parser = getParser(semi_expr)
            d_tree = d_parser.parse()
            result = isContinuous(d_parser, d_tree, value_dict)
    return result


def isContinuous(parser,tree, value):
    alpha = 10**-5
    tolerance = alpha * 10000
    first_variable = list(value.keys())[0]
    try:
        parser.insertValue(value)
        mid = tree.eval()
    except:
        return False
    #check x_axis
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]-alpha
    parser.insertValue(temp)
    left = tree.eval()
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]+alpha
    parser.insertValue(temp)
    right = tree.eval()
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
                    val = d_tree.eval()
                    result = True
                except:
                    result = False
    return result


def plot2D(parser, tree, start, end):
    values = np.linspace(start, end , 1000)
    x = []
    y = []
    variables = list(parser.getVariables().keys())
    first_variable = variables[0] if len(variables) > 0 else 'No_Variable'
    value_dict = {}

    for value in values:
        value_dict[first_variable] = value
        if isContinuous(parser,tree, value_dict):
            parser.insertValue(value_dict)
            mid = tree.eval()
            x.append(value)
            y.append(mid)
        else:
            x.append(np.nan)
            y.append(np.nan)
                   

    x = np.asarray(x)
    y = np.asarray(y)
    return [x,y]

def plot3D(parser, tree, start, end):
    values = np.linspace(start, end, 50)
    real_x = []
    real_y = []
    real_z = []
    flag = 0
    variables = list(parser.getVariables().keys())

    first_variable = variables[0]
    second_variable = variables[1]
    value_dict = {}
    flag = 0
    for value_x in values[:]:
        z = []
        y = []
        x = []
        outer_value = None
        inner_value = None
        value_dict[first_variable] = value_x
        for value_y in values[:]:
            value_dict[second_variable] = value_y
            if isContinuous(parser,tree,value_dict):
                parser.insertValue(value_dict)
                mid = tree.eval()
                x.append(value_x)
                y.append(value_y)            
                z.append(mid)
            else:
                x = np.nan
                y = np.nan
                z.append(np.nan)

        real_x.append(x)
        real_y.append(y)
        real_z.append(z)
    x= np.asarray(real_x)
    y= np.asarray(real_y)
    z= np.asarray(real_z)
    return [x,y,z]

def draw2D(data, figure_num, title):
    x,y = data
    fig = plt.figure(figure_num)
    ax = plt.axes()
    ax.set_xlabel('x')
    ax.set_ylabel('y',rotation=0)
    vmin = np.nanmin(y)-0.1; vmax = np.nanmax(y)
    plt.ylim(vmin, vmax)
    plt.title(title)
    plt.plot(x,y)
    plt.close()
    return mpld3.fig_to_html(fig,template_type ='simple')

def draw3D(data, figure_num, title):
    mpl.rcParams['legend.fontsize'] = 10
    x,y,z = data
    fig = plt.figure(figure_num)
    ax = plt.gca(projection='3d')
    plt.title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.contour3D(x, y, z, 50)
    vmin = np.nanmin(y)-0.1; vmax = np.nanmax(y)
    plt.ylim(vmin, vmax)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)


def getParser(case):
    scanner = Scanner(case)
    parser = Parser(scanner)
    return parser

def caculate(case,value):
    value_dict = {}
    for element in value:
        symbol, point = element.split('=')
        value_dict[symbol] = float(point)
    
    parser = getParser(case)
    tree = parser.parse()
    parser.insertValue(value_dict)
    return tree.eval()
def test3(case,value):
    parser = getParser(case)
    tree = parser.parse()
    canonicalization = tree.canonicalize()
    print(canonicalization)
    parser.insertValue(value)
    print(tree.eval())
    derivatives = parser.getDerivative(tree)
    print(derivatives)
def test2(case, start_end):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    if isinstance(tree, Error):
        return [], tree, [], []
    canonicalization = tree.canonicalize()
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
            pics.append(draw3D(data, figure_num, canonicalization))  
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


def test(case, start_end, derivative_points):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    
    if isinstance(tree, Error):
        return [], tree, [], [], []
    
    
    canonicalization = tree.canonicalize()
    canonicalization = list2str(canonicalization)
    if canonicalization[0] == '(' and canonicalization[-1] == ')': canonicalization = canonicalization[1:-1]
    
    try:
        variable_num = len(parser.getVariables())
        start, end = start_end
        figure_num = 1
        if not isinstance(canonicalization, (int,float)):
            if variable_num > 1:
                data = plot3D(parser, tree, start, end)
                pics.append(draw3D(data, figure_num, canonicalization))  
            elif variable_num == 1:
                data = plot2D(parser, tree, start, end)
                pics.append(draw2D(data, figure_num, canonicalization))    
    except Exception as e:
        return [e], tree, [], [], []
    
    try:
        # derivatives = parser.getDerivative(tree)
        derivatives = getDerivative(parser, tree)
        if derivativeAtPoint(parser,tree,derivative_points,derivatives):
            derivative_points = derivative_points + [' is Valid']
        else:
            derivative_points = derivative_points + [' is invalid']
        
        derivative_points = list2str(derivative_points)
    except Exception as e:
        return  pics. canonicalization, [],[], e
    
    try:
        domain = list(parser.getDomain())
        if derivatives is None:
            derivatives = []
        if derivatives is not None:
            for d in derivatives:
                d[1] = list2str(d[1])
                figure_num += 1
                semi_expr = list2str(d[1])
                partial_derivatives.append(list2str(d))
                d_parser = getParser(semi_expr)
                d_tree = d_parser.parse()
                d_title = semi_expr
                d_variable_num = len(d_parser.getVariables())
                if d_variable_num > 1:
                    d_data = plot3D(d_parser, d_tree, start, end)
                    pics.append(draw3D(d_data, figure_num, d_title))
                else:
                    d_data = plot2D(d_parser, d_tree, start, end)
                    pics.append(draw2D(d_data, figure_num, d_title))
        clean_domain = []
        for d in domain:
            clean_domain.append(list2str(d))
        if len(clean_domain) == 0: clean_domain.append('R')
    except Exception as e:
        return pics, canonicalization, [e], [e], derivative_points 

    return pics, canonicalization, partial_derivatives, clean_domain, derivative_points





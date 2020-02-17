import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from calculator.parser import Parser
from calculator.scanner import Scanner
import matplotlib.pyplot as plt, mpld3
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import io
import base64
mpl.use('Agg')
from copy import deepcopy

def derivativeAtPoint(parser,tree,value, derivatives):
    # value_dict = {}
    # for element in value:
    #     symbol, point = element.split('=')
    #     value_dict[symbol] = float(point)
    value_dict = value
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


def isContinuous(tree, value):
    alpha = 10**-5
    tolerance = alpha * 10000
    first_variable = list(value.keys())[0]
    try:
        mid = tree.eval(value)
    except:
        return False
    #check x_axis
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]-alpha
    left = tree.eval(temp)
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]+alpha
    right = tree.eval(temp)
    return abs(left-mid)<tolerance and abs(mid-right)<tolerance


def plot2D(tree, start, end):
    values = np.linspace(start, end , 1000)
    x = []
    y = []
    variables = list(tree.getVariables())
    first_variable = variables[0] if len(variables) > 0 else 'No_Variable'
    value_dict = {}

    for value in values:
        value_dict[first_variable] = value
        if isContinuous(tree, value_dict):
            mid = tree.eval(value_dict)
            x.append(value)
            y.append(mid)
        else:
            x.append(np.nan)
            y.append(np.nan)
                   

    x = np.asarray(x)
    y = np.asarray(y)
    return [x,y]

def plot3D(tree, start, end):
    values = np.linspace(start, end, 80)
    real_x = []
    real_y = []
    real_z = []
    flag = 0
    variables = list(tree.getVariables())
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
            if isContinuous(tree,value_dict):
                mid = tree.eval(value_dict)
                x.append(value_x)
                y.append(value_y)            
                z.append(mid)
            else:
                x.append(np.nan)
                y.append(np.nan)
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
    vmin = np.nanmin(y)-0.1; vmax = np.nanmax(y)+0.1
    plt.ylim(vmin, vmax)
    plt.title(title)
    plt.plot(x,y)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

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

def test(case, start_end, derivative_points,value):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    canonicalization = tree.canonicalize()
    calculation = canonicalization.eval(value)
    
    variables = canonicalization.getVariables()
    variable_num = len(variables)
    start, end = start_end
    figure_num = 1
    if variable_num > 1:
        data = plot3D(canonicalization, start, end)
        pics.append(draw3D(data, figure_num, canonicalization))  
    elif variable_num == 1:
        data = plot2D(canonicalization, start, end)
        pics.append(draw2D(data, figure_num, canonicalization))   
    for symbol in variables:
        d_tree = canonicalization.getDerivative(symbol)
        partial_derivatives.append(f'd({canonicalization})/d{symbol} = {d_tree}')
        d_variables = d_tree.getVariables()
        d_variable_num = len(d_variables)
        if d_variable_num > 1:
            data = plot3D(d_tree, start, end)
            pics.append(draw3D(data, figure_num, d_tree))  
        elif d_variable_num == 1:
            data = plot2D(d_tree, start, end)
            pics.append(draw2D(data, figure_num, d_tree))   
    return pics, canonicalization, partial_derivatives, [], [], calculation






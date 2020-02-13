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

#사용안함
def checkDomain(parser,tree, value):
    domain = parser.getDomain()
    parser.insertValue(value)
    validity = True
    for symbol, rule in domain:
        rule_op, invalid_value = rule.split(',')
        try:
            test_value = symbol.eval()
        except:
            return False
        validity &= domainRule[rule_op](test_value, float(invalid_value))
    return validity

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
        tree.insertValue(value)
        mid = tree.eval()
    except:
        return False
    #check x_axis
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]-alpha
    tree.insertValue(temp)
    left = tree.eval()
    temp = deepcopy(value)
    temp[first_variable] = temp[first_variable]+alpha
    tree.insertValue(temp)
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


def plot2D(tree, start, end):
    values = np.linspace(start, end , 1000)
    x = []
    y = []
    variables = list(tree.getVariables().keys())
    print(variables, 'plot2d')
    first_variable = variables[0] if len(variables) > 0 else 'No_Variable'
    value_dict = {}

    for value in values:
        value_dict[first_variable] = value
        print(value_dict)
        if isContinuous(tree, value_dict):
            tree.insertValue(value_dict)
            mid = tree.eval()
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
    variables = list(tree.getVariables().keys())
    print(variables, 'plot3d')
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
                tree.insertValue(value_dict)
                mid = tree.eval()
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
    # plt.close()
    # return mpld3.fig_to_html(fig,template_type ='simple')

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
    value_dict = value
    parser = getParser(case)
    tree = parser.parse()
    parser.insertValue(value_dict)
    return tree.eval()

def test(case, start_end, derivative_points,value):
    pics = []
    partial_derivatives = []
    parser = getParser(case)
    tree = parser.parse()
    canonicalization = tree.canonicalize()
    canonicalization.insertValue(value)
    calculation = canonicalization.eval()
    
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
        d_variables = d_tree.countVariable()
        d_variable_num = len(d_variables)
        print(d_tree)
        if d_variable_num > 1:
            data = plot3D(d_tree, start, end)
            pics.append(draw3D(data, figure_num, d_tree))  
        elif d_variable_num == 1:
            data = plot2D(d_tree, start, end)
            pics.append(draw2D(data, figure_num, d_tree))   
    return pics, canonicalization, partial_derivatives, [], [], calculation

# def test(case, start_end, derivative_points):
#     pics = []
#     partial_derivatives = []
#     parser = getParser(case)
#     tree = parser.parse()
    
#     if isinstance(tree, Error):
#         return [], tree, [], [], []
    
    
#     canonicalization = tree.canonicalize()
#     canonicalization = list2str(canonicalization)
#     if canonicalization[0] == '(' and canonicalization[-1] == ')': canonicalization = canonicalization[1:-1]
    
#     try:
#         variable_num = len(parser.getVariables())
#         start, end = start_end
#         figure_num = 1
#         if not isinstance(canonicalization, (int,float)):
#             if variable_num > 1:
#                 data = plot3D(parser, tree, start, end)
#                 pics.append(draw3D(data, figure_num, canonicalization))  
#             elif variable_num == 1:
#                 data = plot2D(parser, tree, start, end)
#                 pics.append(draw2D(data, figure_num, canonicalization))    
#     except Exception as e:
#         # raise e
#         return [e], canonicalization, [], [], []
    
#     try:
#         expression_variables = parser.getVariables()
#         derivatives = getDerivative(parser, tree)
#         derivative_points_result = []
#         if derivativeAtPoint(parser,tree,derivative_points,derivatives):
#             for vari in expression_variables.keys():
#                 for deri in derivative_points.keys():
#                     if vari == deri:
#                         derivative_points_result.append(deri+ '='+ str(derivative_points[deri])+' is Valid')
#             # derivative_points = derivative_points + [' is Valid']
#         else:
#             for vari in expression_variables.keys():
#                 for deri in derivative_points.keys():
#                     if vari == deri:
#                         derivative_points_result.append(deri+ '='+ str(derivative_points[deri])+' is invalid')
#             # derivative_points = derivative_points + [' is invalid']
        
#         # derivative_points = list2str(derivative_points)
#     except Exception as e:
#         raise e
#         return  pics, canonicalization, [],[], [e]
    
#     try:
#         domain = list(parser.getDomain())
#         if derivatives is None:
#             derivatives = []
#         if derivatives is not None:
#             for d in derivatives:
#                 d[1] = list2str(d[1])
#                 figure_num += 1
#                 semi_expr = list2str(d[1])
#                 partial_derivatives.append(list2str(d))
#                 d_parser = getParser(semi_expr)
#                 d_tree = d_parser.parse()
#                 d_title = semi_expr
#                 d_variable_num = len(d_parser.getVariables())
#                 print(d_variable_num)
#                 if d_variable_num > 1:
#                     d_data = plot3D(d_parser, d_tree, start, end)
#                     pics.append(draw3D(d_data, figure_num, d_title))
#                 else:
#                     d_data = plot2D(d_parser, d_tree, start, end)
#                     pics.append(draw2D(d_data, figure_num, d_title))
#         clean_domain = []
#         for d in domain:
#             clean_domain.append(list2str(d))
#         if len(clean_domain) == 0: clean_domain.append('R')
#     except Exception as e:
#         return pics, canonicalization, [e], [e], derivative_points_result
#     print('pics',len(pics))
#     return pics, canonicalization, partial_derivatives, clean_domain, derivative_points_result
#     # return pics, canonicalization, partial_derivatives, clean_domain, derivative_points





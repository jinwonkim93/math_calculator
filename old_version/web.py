
from flask import Flask, redirect, url_for, request, render_template,make_response
from single_test import test, caculate
import os
import subprocess
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

def cleanLine(line):
    result_dict = {}
    result = line.replace(' ', '')
    result = result.split(',')
    for element in result:
        symbol, value = element.split('=')
        result_dict[symbol] = float(value)
    return result_dict
@app.route('/input', methods = ['POST', 'GET'])
def calcExpr():
   if request.method == 'POST':
      expr = request.form['Expression']
      expr_range = request.form['Range']
      derivative_points = request.form['Point']
      calculation = request.form['Calculation']
      
      if expr_range == '': expr_range = '-1,1'
      if derivative_points == '': derivative_points = 'x=1,y=1'
      if calculation =='': calculation = 'x=1,y=1'
      
      derivative_points = cleanLine(derivative_points)
      calculation = cleanLine(calculation)
      expr_range = list(map(float,expr_range.split(',')))
      calculation_result = caculate(expr,calculation)
      pics, canonicalization, partial_derivatives, domain, derivative_point = test(expr,expr_range,derivative_points)
      return render_template('image.html',
                             pics = pics,
                             canonicalization = canonicalization,
                             input = expr,
                             result = calculation_result,
                             partial_derivatives = partial_derivatives,
                             domain = domain,
                             derivative_point = derivative_point)


@app.route("/")
def main():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug = True)
    #app.run()



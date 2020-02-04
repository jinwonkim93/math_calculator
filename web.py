
from flask import Flask, redirect, url_for, request, render_template,make_response
from single_test import test
import os
import subprocess
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

@app.route('/input', methods = ['POST', 'GET'])
def calcExpr():
   if request.method == 'POST':
      expr = request.form['Expression']
      expr_range = request.form['Range']
      derivative_points = request.form['Point']
      if expr_range == '': expr_range = '-1,1'
      if derivative_points == '': derivative_points = 'x=1,y=1'
      derivative_points = derivative_points.replace(' ', '')
      expr_range = list(map(float,expr_range.split(',')))
      derivative_points = derivative_points.split(',')
      pics, canonicalization, partial_derivatives, domain, derivative_point = test(expr,expr_range,derivative_points)
      return render_template('image.html',
                             pics = pics,
                             canonicalization = canonicalization,
                             input = expr,
                             partial_derivatives = partial_derivatives,
                             domain = domain,
                             derivative_point = derivative_point)


@app.route("/")
def main():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug = True)
    #app.run()



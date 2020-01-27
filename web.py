
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
      if expr_range == '': expr_range = '-1,1'
      expr_range = list(map(int,expr_range.split(',')))
      pics, canonicalization, partial_derivatives, domain = test(expr,expr_range)
      return render_template('image.html',
                             pics = pics,
                             canonicalization = canonicalization,
                             input = expr,
                             partial_derivatives = partial_derivatives,
                             domain = domain)


@app.route("/")
def main():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug = True)
    #app.run()



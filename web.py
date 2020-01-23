
from flask import Flask, redirect, url_for, request, render_template,make_response
from single_test import test
import os
import subprocess
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response      
  return update_wrapper(no_cache, view)
###############

@app.route('/input', methods = ['POST', 'GET'])
@nocache
def calcExpr():
   if request.method == 'POST':
      expr = request.form['Expression'] 
      expr_range = request.form['Range'].split('~')
      return_code = subprocess.call("rm ./static/2.0*x2d.png", shell=True)
      print(return_code)
      pics, canonicalization, partial_derivatives, domain = test(expr)
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




from flask import Flask, redirect, url_for, request, render_template
from calculator2 import run_calc
app = Flask(__name__)

@app.route("/calc", methods = ['POST', 'GET'])
def calc():
    if request.method == 'POST':
        expression = request.form['expression']
        result, postfix = run_calc(expression)
        return render_template('index.html',answer = result, postfix = postfix)


@app.route("/")
def main():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug = True)
    #app.run()



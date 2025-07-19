from flask import Flask, render_template, request
import sys
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def submit():
    data = request.form
    code = data['code']
    return render_template('index.html', result=run_code(code))

def run_code(code):
    # Redirect the output to a string
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        # shhh
        exec(code)
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        return e
    
    return redirected_output.getvalue()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

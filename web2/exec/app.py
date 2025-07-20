from flask import Flask, request, render_template_string
import ast
import operator as op

app = Flask(__name__)

# Supported operators mapping
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

def safe_eval(node):
    """
    Recursively evaluate an AST limited to safe numeric operations.
    """
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        oper = operators.get(type(node.op))
        if oper is None:
            raise ValueError('Unsupported operator: {}'.format(node.op))
        return oper(left, right)
    raise ValueError('Unsupported expression type')

@app.route('/', methods=['GET','POST'])
def index():
    result = ''
    if request.method == 'POST':
        expr = request.form.get('code','')
        try:
            parsed = ast.parse(expr, mode='eval')
            result = safe_eval(parsed.body)
        except Exception as e:
            result = 'Error: {}'.format(e)
    return render_template_string(
        '''
        <form method="post">
          <input name="code" value="{{ request.form.code }}">
          <input type="submit" value="Evaluate">
        </form>
        <div>Result: {{ result }}</div>
        ''', result=result)

if __name__ == '__main__':
    app.run()
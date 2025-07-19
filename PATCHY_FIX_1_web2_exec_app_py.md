# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Removed use of exec() for direct arbitrary code execution. Instead implemented a safe arithmetic expression evaluator using Python's ast module, which parses and evaluates only arithmetic expressions with a whitelist of allowed operators. This prevents execution of arbitrary code from user input, mitigating code injection risk.

## Security Notes
Avoid use of exec()/eval on user inputs. Use safe parsers or expression evaluators with strict whitelisting. Always validate and sanitize user inputs thoroughly.

## Fixed Code
```py
from flask import Flask, request, jsonify
app = Flask(__name__)

# Instead of using exec() on user input, define a safe evaluator or whitelist commands
@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.form.get('code', '')

    # For demonstration, we will limit to evaluating arithmetic expressions safely using ast
    import ast, operator

    # Mapping of allowed operators
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg
    }

    def eval_expr(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in allowed_operators:
                raise ValueError('Operator not allowed')
            return allowed_operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in allowed_operators:
                raise ValueError('Operator not allowed')
            return allowed_operators[type(node.op)](eval_expr(node.operand))
        else:
            raise ValueError('Unsupported expression')

    try:
        expr_ast = ast.parse(user_code, mode='eval').body
        result = eval_expr(expr_ast)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import ast
- import operator

## Testing Recommendations
- Test with valid arithmetic expressions returns correct results.
- Test with malicious code snippets returns errors, no code execution.
- Test with edge cases (empty input, very large numbers).

## Alternative Solutions

### Implement a custom domain-specific language interpreter with strict syntax checking.
**Pros:** Gives more control over allowed expressions., Easier to add specific business logic validations.
**Cons:** More development effort required., Complex to maintain.

### Use third-party libraries designed for safe expression evaluation like 'asteval'.
**Pros:** Less code to maintain., Well tested for safe evaluation.
**Cons:** Dependency on external libraries., Need to assess library security.


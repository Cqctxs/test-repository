# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used exec() on user-supplied input, which can execute arbitrary code and lead to code execution vulnerabilities. The fix replaces exec() with a safe expression evaluator that only supports arithmetic operations using Python ast parsing and operator whitelist to prevent arbitrary code execution.

## Security Notes
Avoid using exec or eval with user inputs. Use strict parsing and whitelist allowed operations to safely evaluate expressions. Also, handle exceptions gracefully.

## Fixed Code
```py
# Revised app.py in web2/exec to safely evaluate expressions without exec
from flask import Flask, request, jsonify
import ast
import operator as op

app = Flask(__name__)

# Supported operators for safe evaluation
allowed_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}

def safe_eval(expr):
    """Safely evaluate an arithmetic expression from user input."""
    def eval_node(node):
        if isinstance(node, ast.Num): # <number>
            return node.n
        elif isinstance(node, ast.BinOp): # <left> <operator> <right>
            operator = allowed_operators.get(type(node.op))
            if operator is None:
                raise ValueError("Unsupported operator")
            return operator(eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp): # - <operand> e.g. -1
            operator = allowed_operators.get(type(node.op))
            if operator is None:
                raise ValueError("Unsupported unary operator")
            return operator(eval_node(node.operand))
        else:
            raise ValueError("Unsupported expression")

    node = ast.parse(expr, mode='eval').body
    return eval_node(node)

@app.route('/calculate', methods=['POST'])
def calculate():
    expr = request.form.get('expression', '')
    try:
        result = safe_eval(expr)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- operator
- flask

## Testing Recommendations
- Test with valid arithmetic expressions to confirm correct evaluation.
- Test with malicious or malformed input to confirm rejection and no code execution.

## Alternative Solutions

### Use a sandboxed environment or library such as 'asteval' or restricted Python interpreters for evaluated expressions.
**Pros:** Safer than exec, More flexible than custom parser
**Cons:** Adds dependencies, Might be complex to configure

### Limit input to predefined operations or commands rather than free expressions.
**Pros:** Max control, Very safe
**Cons:** Less feature-rich for users


# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code executed arbitrary Python code from user input, which allows remote code execution. The fix eliminates direct use of exec or eval on user input. Instead, a safe_eval function parses the expression using the abstract syntax tree (AST) module and permits only numeric literals and safe mathematical operators. This prevents execution of arbitrary or malicious code, mitigating the vulnerability while maintaining the expression evaluation feature.

## Security Notes
Avoid exec/eval with user inputs. Use safe expression evaluators or domain-specific parsers to evaluate user data. Limit operations to a white-listed set. Ensure input is sanitized and properly parsed.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

# Safe eval implementation to avoid arbitrary code execution
# We define allowed operators and parse the expression safely
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.left), _eval(node.right))
            else:
                raise ValueError('Unsupported operator')
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.operand))
            else:
                raise ValueError('Unsupported unary operator')
        else:
            raise ValueError('Unsupported expression')

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        result = safe_eval(expr)
        return jsonify({'result': result})
    except Exception:
        # On failure, return an error, do not execute code
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- operator

## Testing Recommendations
- Test with valid mathematical expressions to ensure correct results.
- Test with malicious inputs like 'os.system("rm -rf /")' to ensure they're rejected.
- Test with unexpected types (e.g., strings) to verify error handling.

## Alternative Solutions

### Use a third-party library like 'asteval' or 'numexpr' to safely evaluate expressions.
**Pros:** Provides tested safe evaluation with broader features.
**Cons:** Adds external dependency., May still require input validation.

### Restrict user inputs to predefined commands or formulas, avoiding direct expression evaluation.
**Pros:** Eliminates code execution entirely., Easier to control inputs.
**Cons:** Less flexible for users., Requires redesign of user interaction.


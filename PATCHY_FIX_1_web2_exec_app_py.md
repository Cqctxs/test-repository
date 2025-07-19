# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original vulnerable code executed arbitrary code from user input using exec(), which allows full remote code execution. The fix replaces that with a safe expression evaluator that only allows simple arithmetic operations by parsing the expression securely (using Python's ast module) and explicitly controlling which operators can be used. This prevents execution of arbitrary code. The new code only evaluates safe arithmetic expressions, returning errors for invalid or unsafe input.

## Security Notes
Never use exec or eval on user input. Always prefer safe parsing and evaluation techniques. Use parsing libraries or domain-specific validators depending on input context. Refrain from exposing raw code execution interfaces publicly. Run the app without debug mode to avoid information leaks.

## Fixed Code
```py
import ast
import operator as op
from flask import Flask, request, jsonify

app = Flask(__name__)

# Supported operators for safe evaluation
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg
}

def safe_eval(expr):
    '''Safely evaluate a user-provided arithmetic expression.'''
    def eval_(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return operators[type(node.op)](eval_(node.left), eval_(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return operators[type(node.op)](eval_(node.operand))
        else:
            raise TypeError('Unsupported type')
    try:
        node = ast.parse(expr, mode='eval').body
        return eval_(node)
    except Exception:
        raise ValueError('Invalid expression')

@app.route('/evaluate', methods=['POST'])
def evaluate_code():
    user_input = request.form.get('expr', '')
    try:
        result = safe_eval(user_input)
    except ValueError:
        return jsonify({'error': 'Invalid input expression'}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast
- import operator as op

## Testing Recommendations
- Test with valid arithmetic expressions to ensure correct output.
- Test with malicious input such as system commands to ensure rejection.
- Test empty or malformed input to verify error handling.

## Alternative Solutions

### Use a restricted environment sandbox such as 'restrictedpython' library to safely execute code.
**Pros:** More flexible than hardcoded safe_eval function, Supports more Python syntax if needed
**Cons:** Adds dependency, May still be complex to configure securely

### Avoid user code execution entirely and redesign the app to receive structured inputs with predefined operations.
**Pros:** Eliminates code execution risk entirely, Simplifies security model
**Cons:** May limit application functionality, Requires changes to user interface


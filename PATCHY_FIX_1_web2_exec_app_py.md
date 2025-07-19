# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
The original code executed arbitrary code from user input via exec or eval, leading to remote code execution vulnerability. This fix replaces the unsafe eval/exec with a safe expression evaluator `safe_eval` that only permits numeric operations and forbids arbitrary code execution. This approach uses Python's AST to parse and whitelist allowed operations to prevent code injection.

## Security Notes
Using `eval` or `exec` on user input is extremely unsafe. By parsing the expression and permitting only safe mathematical operations, we mitigate the risk of arbitrary code execution. In real applications, consider even more restrictive parsing or dedicated libraries. Always sanitize and validate user inputs.

## Fixed Code
```py
# web2/exec/app.py
from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

# Allowed operators mapping for safe_eval
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
    """Safely evaluate a mathematical expression.
    This function parses the expression AST and only allows safe operations.
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.left), _eval(node.right))
            else:
                raise ValueError("Unsupported operator")
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.operand))
            else:
                raise ValueError("Unsupported unary operator")
        else:
            raise TypeError("Unsupported expression")

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.form.get('code', '')
    try:
        # Evaluate user_code safely as a mathematical expression rather than arbitrary code execution
        result = safe_eval(user_code)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- operator

## Testing Recommendations
- Test with valid mathematical expressions (e.g., 2+3*4) to confirm correct evaluation.
- Test with invalid or malicious code inputs to confirm they are rejected with error.
- Perform fuzz testing with unexpected input formats.

## Alternative Solutions

### Disallow user-submitted code entirely and only allow predefined commands or operations.
**Pros:** Complete removal of direct code evaluation eliminates this class of vulnerabilities.
**Cons:** Reduced flexibility; may not meet all user needs.

### Use sandboxes or containerization to safely execute user code with strict resource and permission limits.
**Pros:** Allows richer code execution while isolating potential damage.
**Cons:** Complex to implement and maintain; still risk of escape exploits.


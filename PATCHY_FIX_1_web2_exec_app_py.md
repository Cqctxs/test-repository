# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the use of 'exec' on user input with a safe evaluation function 'safe_eval' that only allows basic mathematical expressions using a whitelist of allowed AST nodes and operators. This prevents arbitrary code execution by sanitizing and restricting what code can be run from user input.

## Security Notes
Avoid executing user input directly. Use safe parsing or evaluation libraries. Always whitelist allowed operations or commands and never use exec or eval with untrusted data.

## Fixed Code
```py
from flask import Flask, request, jsonify
app = Flask(__name__)

# Instead of using exec on user provided code, define safe allowed operations
# We create a whitelist of allowed commands or use a safe evaluation method
# For this example, we only allow calculation expressions using ast.literal_eval
import ast
import operator

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg,
}

def safe_eval(expr):
    """Safely evaluate a mathematical expression."""
    def eval_node(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):
            return ALLOWED_OPERATORS[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ALLOWED_OPERATORS[type(node.op)](eval_node(node.operand))
        else:
            raise ValueError("Unsupported expression")

    node = ast.parse(expr, mode='eval').body
    return eval_node(node)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    try:
        result = safe_eval(expression)
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
- Test with valid and invalid math expressions.
- Verify that code injection attempts fail and return errors.
- Perform security scans to confirm exec usage is removed.

## Alternative Solutions

### Use a domain-specific language parser that only supports required safe operations.
**Pros:** Fine-grained control over allowed operations., Easier to maintain strict security policies.
**Cons:** Requires implementing or integrating a DSL parser., More complex to develop.

### Sandbox user code execution using containerization or external services.
**Pros:** Reduced risk to main server., Allows more flexibility in running user code.
**Cons:** More infrastructure complexity., Potential performance overhead.


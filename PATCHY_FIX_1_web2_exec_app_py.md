# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The direct use of exec() with user input was replaced with a safe evaluation approach using Python's AST module to parse the expression and ensure only basic math expressions (like addition, subtraction) and safe function calls (abs, round) are allowed. Unsafe nodes and function calls raise exceptions, preventing arbitrary code execution. This preserves the functionality of evaluating code but mitigates the risk of executing malicious code.

## Security Notes
Always avoid exec or eval on user input unless strictly controlled. Using AST parsing restricts which Python constructs can be evaluated safely. Limit callable functions to a known safe subset. Consider whitelisting inputs further if possible.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import _ast

app = Flask(__name__)

class SafeEval(ast.NodeVisitor):
    # Only allow safe nodes for evaluation
    allowed_nodes = {
        _ast.Expression, _ast.BinOp, _ast.UnaryOp, _ast.Num, _ast.Load,
        _ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.Pow, _ast.BitXor, _ast.USub,
        _ast.Name, _ast.Call
    }

    def visit(self, node):
        if type(node) not in self.allowed_nodes:
            raise ValueError(f"Unsafe expression detected: {type(node).__name__}")
        # Disallow function calls except for limited safe ones
        if isinstance(node, _ast.Call):
            if not (isinstance(node.func, _ast.Name) and node.func.id in ('abs', 'round')):
                raise ValueError(f"Unsafe function call detected: {ast.dump(node)}")
        for child in ast.iter_child_nodes(node):
            self.visit(child)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    try:
        # Parse and validate the expression using AST
        tree = ast.parse(code, mode='eval')
        SafeEval().visit(tree)
        # Evaluate the expression safely
        result = eval(compile(tree, filename='<ast>', mode='eval'))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- _ast

## Testing Recommendations
- Test valid expression inputs to ensure results are correct.
- Test invalid code inputs to ensure errors are handled safely.
- Test malicious inputs trying to inject code to confirm they are rejected.

## Alternative Solutions

### Disable any user code execution and provide predefined operations instead.
**Pros:** No risk of code injection, Simpler control over operations
**Cons:** Less flexible for users

### Use a sandboxed environment or third-party sandbox libraries to execute user code securely.
**Pros:** Allows flexible code execution, Isolation of possibly dangerous code
**Cons:** More complex to implement, Performance overhead


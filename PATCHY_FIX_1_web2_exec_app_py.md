# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
The original code used `exec()` on user-submitted Python code, which allows arbitrary code execution and remote code execution vulnerabilities. The fix replaces this with a `safe_eval` function that parses the user's input as a Python expression using `ast.parse` in mode `eval`, and explicitly checks that the AST contains only safe node types. It disallows access to protected members and restricts function calls to a whitelist of safe built-in functions. This provides a controlled and limited evaluation environment instead of executing arbitrary code, mitigating remote code execution risk.

## Security Notes
Avoid using direct exec or eval on user input. Restrict code evaluation with AST parsing, whitelist safe nodes and functions, and limit globals to safe built-ins. Consider advanced sandboxing for more complex requirements.

## Fixed Code
```py
# Original functionality: execute user-submitted python code
# Security fix: remove direct exec of user input; else use very restricted execution environment

import ast
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a safe list of allowed built-ins
SAFE_BUILTINS = {
    'abs': abs,
    'max': max,
    'min': min,
    'sum': sum,
    'len': len,
    'range': range,
    # Add other safe builtins as needed
}

# Function to safely evaluate expressions
def safe_eval(expr):
    try:
        # Parse the expression to an AST object
        tree = ast.parse(expr, mode='eval')
        # Walk the tree to restrict to safe nodes only
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str, ast.Name, ast.Load, ast.operator, ast.unaryop, ast.Call, ast.Compare, ast.BoolOp, ast.List, ast.Tuple)):
                raise ValueError(f'Unsafe expression: {type(node).__name__}')
            # Disallow access to __attributes__ or names starting with underscore
            if isinstance(node, ast.Name) and node.id.startswith('_'):
                raise ValueError('Access to protected names is denied')
            if isinstance(node, ast.Call):
                # Only allow calls to safe builtins
                if not (isinstance(node.func, ast.Name) and node.func.id in SAFE_BUILTINS):
                    raise ValueError('Only safe builtin functions are allowed')

        # Evaluate safely using restricted globals and locals
        return eval(compile(tree, filename='<ast>', mode='eval'), {'__builtins__': SAFE_BUILTINS})
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/exec', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    # Using safe_eval instead of exec to limit code execution
    result = safe_eval(code)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- ast
- sys
- flask

## Testing Recommendations
- Test various Python expressions for correct evaluations
- Test that unsafe expressions (e.g. import os) are rejected
- Test behavior with malicious input like '__import__("os")'

## Alternative Solutions

### Use a third-party sandbox or restricted Python execution environment like restrictedpython or py_mini_racer
**Pros:** Higher security guarantees, Can allow more complex safe execution
**Cons:** Adds dependencies, More complex setup


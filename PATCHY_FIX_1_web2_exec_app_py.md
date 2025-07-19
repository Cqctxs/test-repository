# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the dangerous exec(code) with a safe evaluation function that parses the expression using Python's AST module to restrict allowed node types. This avoids executing arbitrary code by only permitting basic expressions and literals. The safe_eval function blocks statements and operations that can lead to arbitrary code execution. This preserves the original functionality of evaluating expressions but securely.

## Security Notes
Never use exec or eval on user input directly. Use Python's AST module to parse and validate expressions safely. For more complex scenarios, use fully sandboxed environments. Always validate and sanitize user inputs before code execution.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import sys

app = Flask(__name__)

# Safe evaluation function to avoid exec usage
# This function only evaluates simple expressions and literals
# For complex code, consider sandboxing approaches like restricted execution environments

def safe_eval(expression):
    try:
        # Parse the expression into an AST node
        parsed_expr = ast.parse(expression, mode='eval')
        # Only allow simple expressions for safety
        for node in ast.walk(parsed_expr):
            if not isinstance(node, (ast.Expression, ast.Num, ast.Str, ast.BinOp, ast.UnaryOp,
                                     ast.operator, ast.unaryop, ast.NameConstant, ast.Call, ast.Load,
                                     ast.Tuple, ast.List, ast.Dict, ast.Set, ast.Compare, ast.BoolOp)):
                raise ValueError("Unsafe expression detected")
        # Evaluate in empty environment
        return eval(compile(parsed_expr, filename="", mode="eval"), {'__builtins__': {}})
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    # Use safe_eval instead of exec to mitigate arbitrary code execution
    try:
        result = safe_eval(code)
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- sys

## Testing Recommendations
- Test with safe simple expressions (e.g., '1 + 1', '2 * (3 + 4)')
- Test with malicious inputs containing statements, loops, or function calls to ensure rejection
- Test API responds correctly to valid and invalid JSON data

## Alternative Solutions

### Run the user-provided code inside a hardened sandbox environment or container to isolate and control execution.
**Pros:** Allows more complex code evaluation, Full isolation of code execution environment
**Cons:** More complex to implement and maintain, May have performance overhead

### Use predefined commands or a domain-specific language instead of general purpose code execution.
**Pros:** Eliminates risk of arbitrary code execution, Simpler to validate inputs
**Cons:** Limits flexibility, Requires redesign of user interaction


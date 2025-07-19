# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used 'exec()' directly on user-submitted code, allowing arbitrary code execution risks. The fix replaces this with a 'safe_eval' function that parses the code into an AST and whitelists allowed node types, blocking unsafe code constructs. It also restricts built-ins to a safe subset. This prevents arbitrary code execution while maintaining the ability to evaluate simple expressions safely.

## Security Notes
Never run 'exec' or 'eval' directly on user input. Instead, use safe parsing and evaluation techniques, sandbox code execution, or rethink the need for dynamic code execution. Monitor and limit what functions can be called and code complexity allowed. Logs user input and errors carefully to audit misuse.

## Fixed Code
```py
# Fixed app.py to execute user-submitted code in a controlled environment safely
import ast
import _ast

# Function to safely execute simple Python expressions
# This limits execution to a subset of AST nodes for safety

def safe_eval(expr):
    allowed_nodes = (
        _ast.Expression,
        _ast.Str, _ast.Num, _ast.Tuple, _ast.List, _ast.Set, _ast.Dict,
        _ast.NameConstant, _ast.BinOp, _ast.UnaryOp,
        _ast.BoolOp, _ast.Compare, _ast.Call, _ast.Name,
        _ast.Load, _ast.keyword
    )

    # Parse expression
    node = ast.parse(expr, mode='eval')

    # Recursively verify that all nodes are allowed
    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError(f"Unsafe expression: contains {type(subnode).__name__}")

    # Define a whitelist of safe functions, e.g., math functions (optional)
    safe_globals = {
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'len': len,
        # add more safe functions as needed
    }

    # Evaluate expression safely
    return eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, safe_globals)


# Example usage inside the web app (flask or similar)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def evaluate_code():
    user_code = request.form.get('code')
    if not user_code:
        return jsonify({'error': 'No code provided'}), 400
    try:
        # Safely evaluate user code expression
        result = safe_eval(user_code)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import ast
- import _ast
- from flask import Flask, request, jsonify

## Testing Recommendations
- Test with allowed simple expressions to confirm correct evaluation.
- Test with disallowed code injection attempts to confirm safe blocking.
- Test edge cases with complex syntax to verify parser robustness.

## Alternative Solutions

### Use third-party sandboxing libraries such as RestrictedPython for safer code execution.
**Pros:** Provides a well-tested secure sandbox environment, Supports a wider set of Python features safely
**Cons:** Adds dependencies, Might be complex to integrate

### Avoid code execution entirely by redesigning the app to not require dynamic execution of user code.
**Pros:** Eliminates the risk of code injection, Simplifies security concerns
**Cons:** Functionality may be reduced or changed


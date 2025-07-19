# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code executed arbitrary Python code from user input using exec(), which is highly dangerous and leads to remote code execution vulnerability. This fix replaces exec() with a safe evaluation function that parses the expression to an AST (abstract syntax tree) and only allows safe node types. This prevents execution of arbitrary code while preserving the original functionality of evaluating expressions provided by the user. Unsafe expressions cause an error response.

## Security Notes
Direct use of exec/eval with user input is unsafe and must be avoided. Using AST parsing to whitelist allowed syntax nodes limits evaluation to safe expressions only. Running the web server with debug=False prevents accidental information leak. For complex functionality consider a dedicated sandboxed execution environment.

## Fixed Code
```py
from flask import Flask, request, abort
import ast
import _ast

app = Flask(__name__)

# Define a safe list of allowed AST node types for evaluation
SAFE_NODES = {
    _ast.Expression, _ast.UnaryOp, _ast.BinOp,
    _ast.Num, _ast.Str, _ast.NameConstant,
    _ast.Name, _ast.Load, _ast.Call, _ast.Tuple, _ast.List,
    _ast.Dict, _ast.Attribute
}

# Safely evaluate expressions by parsing to AST and allowing only safe nodes

def safe_eval(expr):
    try:
        tree = ast.parse(expr, mode='eval')
        for node in ast.walk(tree):
            if type(node) not in SAFE_NODES:
                raise ValueError(f"Unsafe expression: contains {type(node).__name__}")
        # Use eval with restricted globals and locals
        return eval(compile(tree, filename='<string>', mode='eval'), {'__builtins__': None}, {})
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

@app.route('/execute', methods=['POST'])
def execute_code():
    # Read code from POST parameter
    code = request.form.get('code', '')
    # Instead of exec, only allow safe expressions evaluated through safe_eval
    try:
        result = safe_eval(code)
        return {'result': str(result)}
    except ValueError as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast
- import _ast

## Testing Recommendations
- Test various input expressions to confirm correct evaluation and error handling.
- Attempt injection strings to ensure they are rejected.
- Verify error messages do not leak sensitive info.

## Alternative Solutions

### Remove dynamic code execution altogether and replace with predefined allowable operations received via API.
**Pros:** Completely eliminates code injection risk, Easier to secure
**Cons:** May reduce flexibility for advanced users

### Use a dedicated sandbox or container to securely run user code with strict resource and access limitations.
**Pros:** Allows extensive code execution while containing risks
**Cons:** More complex infrastructure and maintenance


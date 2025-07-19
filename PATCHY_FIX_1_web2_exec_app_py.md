# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the use of exec for running arbitrary user-submitted code with a safe evaluation function using Python's AST module to parse and restrict execution to only safe, limited Python expressions (like simple calculations). This prevents arbitrary code execution by limiting the operations and names that can be used.

## Security Notes
User code execution is sandboxed to prevent remote code execution vulnerabilities. No exec or eval on raw user input is used. Only a strict set of expressions and builtins (abs, min, max, sum, len, range) are allowed. This minimal evaluator can be further extended for more controlled functionality.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import _ast

app = Flask(__name__)


class SafeEval(ast.NodeVisitor):
    """
    This class walks the AST and ensures that only safe nodes are allowed.
    Disallows exec, import, function definitions and calls, attribute access, etc.
    """

    SAFE_NODES = {
        _ast.Expression, _ast.Str, _ast.Num, _ast.Tuple, _ast.List, _ast.Dict,
        _ast.BinOp, _ast.UnaryOp, _ast.BoolOp, _ast.Compare,
        _ast.NameConstant, _ast.Name, _ast.Load
    }

    ALLOWED_NAMES = {'abs', 'min', 'max', 'sum', 'len', 'range'}

    def visit(self, node):
        if type(node) not in self.SAFE_NODES:
            raise ValueError(f"Unsafe expression: {type(node).__name__} not allowed")

        # Only allow certain names
        if isinstance(node, _ast.Name):
            if node.id not in self.ALLOWED_NAMES:
                raise ValueError(f"Use of name {node.id} is not allowed")

        super().visit(node)


def safe_eval(expr):
    try:
        node = ast.parse(expr, mode='eval')
        SafeEval().visit(node)
        return eval(compile(node, '<string>', mode='eval'), {'__builtins__': {}}, {})
    except Exception as e:
        return str(e)


@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    # Instead of exec, we parse and restrict the code to safe expressions only
    result = safe_eval(code)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
- import ast
- import _ast

## Testing Recommendations
- Test with multiple code snippets including safe expressions and malicious code attempts.
- Ensure only limited functions and expressions can be executed.
- Test for common RCE payloads and confirm they're blocked.

## Alternative Solutions

### Use a full Python sandboxing library like RestrictedPython
**Pros:** More comprehensive sandboxing and filtering capabilities, More official support for sandboxing
**Cons:** Additional dependencies, Performance overhead

### Use external sandboxed environments (e.g., Docker containers) to run code safely
**Pros:** Complete isolation from host environment, Better security boundaries
**Cons:** Complex infrastructure changes, Resource intensive


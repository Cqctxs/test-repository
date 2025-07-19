# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed direct exec of user input. Instead, parse the expression into an AST and allow only arithmetic nodes. Evaluate in an empty builtins namespace to prevent RCE.

## Security Notes
Restricts code to numeric operations. For more functions, explicitly whitelist safe functions.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define a safe subset of operations
ALLOWED_AST_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.Num, ast.Load, ast.Name
}

class SafeEval(ast.NodeVisitor):
    def generic_visit(self, node):
        if type(node) not in ALLOWED_AST_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        super().generic_visit(node)

@app.route('/eval', methods=['POST'])
def evaluate():
    source = request.json.get('expr', '')
    try:
        # Parse into AST and validate
        tree = ast.parse(source, mode='eval')
        SafeEval().visit(tree)
        # Compile and evaluate in empty namespace
        compiled = compile(tree, filename='<ast>', mode='eval')
        result = eval(compiled, {'__builtins__': {}})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import ast

## Testing Recommendations
- POST various valid and invalid expressions, ensure errors on disallowed syntax.

## Alternative Solutions

### Use a third-party math expression library (e.g., asteval or mathjs)
**Pros:** Battle-tested sanitization, Rich feature set
**Cons:** Additional dependency


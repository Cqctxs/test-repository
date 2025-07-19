# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used exec() on user-submitted code without sanitization, which causes critical remote code execution risks. The fixed code replaces exec with a safe evaluator that uses Python's ast module to parse and validate the submitted code to only allow an expression and a set of safe operations and functions. It then evaluates the code in a restricted environment with no builtins except for a whitelist of safe functions. This drastically reduces the risk of malicious code execution while maintaining original functionality of evaluating arithmetic or simple expressions.

## Security Notes
Always restrict code execution contexts and validate input AST nodes when evaluating user code. Avoid exec() and eval() with user input. Use allowlists of functions and disallow unsafe AST nodes to prevent code injection.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import _ast

app = Flask(__name__)

class SafeEval(ast.NodeVisitor):
    SAFE_NODES = (
        _ast.Expression, _ast.BinOp, _ast.UnaryOp, _ast.Num, _ast.Str, _ast.NameConstant,
        _ast.Name, _ast.Load, _ast.Call, _ast.Compare, _ast.BoolOp, _ast.List, _ast.Tuple
    )
    SAFE_NAMES = {'abs', 'max', 'min', 'round'}  # whitelist of safe functions

    def visit(self, node):
        if not isinstance(node, self.SAFE_NODES):
            raise ValueError(f"Unsafe expression: {type(node).__name__}")
        return super().visit(node)

    def visit_Name(self, node):
        if node.id not in self.SAFE_NAMES:
            raise ValueError(f"Use of unsafe function or variable: {node.id}")

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    try:
        # Parse the code into AST
        tree = ast.parse(code, mode='eval')
        # Validate AST nodes
        SafeEval().visit(tree)
        # Compile and evaluate the expression safely
        result = eval(compile(tree, filename='<string>', mode='eval'), {'__builtins__': None}, {'abs': abs, 'max': max, 'min': min, 'round': round})
        return jsonify({'result': result})
    except Exception as e:
        # Return error message without sensitive details
        return jsonify({'error': 'Invalid or unsafe code'}), 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast
- import _ast

## Testing Recommendations
- Test code submissions including safe expressions return expected results.
- Test attempted malicious code submissions are rejected with errors and no execution.
- Perform fuzz testing with various inputs to ensure no code injection or crashes.

## Alternative Solutions

### Use a third-party sandboxed code execution environment or containerized solution to safely run arbitrary code submissions.
**Pros:** Isolates execution environment, Allows more flexibility in code execution
**Cons:** Increased complexity, Requires infrastructure setup and maintenance

### Restrict to a domain-specific language or limited command set that only allows predefined operations.
**Pros:** Full control over allowed operations, Minimal risk
**Cons:** Reduced functionality, Requires implementation of custom interpreter


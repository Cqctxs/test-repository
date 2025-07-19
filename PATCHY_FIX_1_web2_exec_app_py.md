# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original app.py directly executed user-submitted code using exec(), which allows arbitrary code execution. The fix replaces this with a safer evaluation approach using Python's AST module to parse the user input and only allow a restricted subset of safe expressions (arithmetic and simple constants). This prevents execution of arbitrary code and mitigates remote code execution vulnerabilities.

## Security Notes
Using AST parsing and checking allowed nodes ensures that only safe Python expressions are executed. The use of eval() is controlled tightly with no built-ins and an empty globals dict. Further hardening can involve using sandboxing or dedicated expression evaluators.

## Fixed Code
```py
import ast
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a safe subset of Python AST nodes that are allowed to execute
ALLOWED_NODES = {
    'Expression', 'BinOp', 'UnaryOp', 'Num', 'Str', 'NameConstant', 'Name',
    'Load', 'Add', 'Sub', 'Mult', 'Div', 'Pow', 'Mod', 'UAdd', 'USub', 'Compare',
    'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'BoolOp', 'And', 'Or', 'IfExp', 'List', 'Tuple'
}

class SafeEval(ast.NodeVisitor):
    def generic_visit(self, node):
        node_name = type(node).__name__
        if node_name not in ALLOWED_NODES:
            raise ValueError(f"Unsafe expression: {node_name} not allowed")
        super().generic_visit(node)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    try:
        # Parse the expression using AST
        tree = ast.parse(code, mode='eval')
        # Check for safety
        SafeEval().visit(tree)
        # Evaluate the expression safely
        result = eval(compile(tree, filename='<ast>', mode='eval'), {'__builtins__': None}, {})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test execution of safe arithmetic expressions (e.g., '1 + 2 * 3').
- Test rejection of unsafe code (e.g., 'import os', '__import__("os")', 'open("file")').
- Test boundary cases like empty input or large expressions.

## Alternative Solutions

### Use a third-party library like 'asteval' that provides a safe subset of Python evaluation.
**Pros:** Provides rich expression evaluation., Less manual parsing code needed.
**Cons:** Adds a dependency., Needs review for specific security guarantees.

### Implement a custom, domain-specific expression parser and evaluator.
**Pros:** Full control over allowed operations., No reliance on Python's eval or AST.
**Cons:** Requires significant development effort., May be less flexible.


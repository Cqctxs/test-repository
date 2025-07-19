# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the direct use of exec on user-submitted code with a safe evaluator that parses and evaluates only arithmetic expressions using the ast module. This avoids executing arbitrary code and mitigates remote code execution vulnerabilities.

## Security Notes
Do not execute or eval arbitrary user input. Instead, use controlled parsing and evaluation or limited domain-specific language interpreters. Consider deploying additional input validation and sanitization before evaluating expressions.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import _ast

app = Flask(__name__)

# Safe evaluation function to allow only arithmetic expressions
class SafeEval(ast.NodeVisitor):
    ALLOWED_NODES = {
        _ast.Expression, _ast.BinOp, _ast.UnaryOp, _ast.Num,
        _ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.Pow, _ast.Mod,
        _ast.USub, _ast.UAdd, _ast.Load, _ast.Constant  # For newer Python versions
    }

    def visit(self, node):
        if type(node) not in self.ALLOWED_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        return super().visit(node)

    def eval(self, expr):
        try:
            tree = ast.parse(expr, mode='eval')
            self.visit(tree)
            return eval(compile(tree, filename="", mode="eval"))
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    try:
        evaluator = SafeEval()
        result = evaluator.eval(code)
        return jsonify({'result': result})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast
- import _ast

## Testing Recommendations
- Test that only allowed arithmetic expressions can be evaluated successfully.
- Attempt to submit malicious code and verify it is rejected.
- Verify error messages do not leak sensitive information.

## Alternative Solutions

### Implement a sandboxed environment using restricted Python interpreters like RestrictedPython or PyPy sandbox.
**Pros:** Provides a more comprehensive sandbox environment., Can run limited subset of Python safely.
**Cons:** More complex to implement and maintain., May impact performance.

### Design and implement a domain-specific language or configuration format instead of executing code.
**Pros:** No arbitrary code execution risks., Easier to validate input.
**Cons:** Requires significant development and user education.


# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced arbitrary execution of user-input Python code with a safe evaluator that only permits literal expressions and basic operations using the ast module. This prevents arbitrary code execution by disallowing function calls, attribute access, imports, or other unsafe nodes.

## Security Notes
Never execute user input as code directly. Use safe parsing and evaluation approaches, restrict allowed operations, and handle errors to avoid leaks. Logs and error messages should not reveal sensitive context.

## Fixed Code
```py
from flask import Flask, request, abort
import ast

app = Flask(__name__)

# Safe evaluation: only allow literal expressions and restricted operations
class SafeEval(ast.NodeVisitor):
    ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str, ast.NameConstant, ast.Load, ast.operator, ast.unaryop)

    def visit(self, node):
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(f'Unsafe expression: {type(node).__name__}')
        return super().visit(node)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code')
    if not code:
        abort(400, 'No code provided')
    
    try:
        parsed = ast.parse(code, mode='eval')
        SafeEval().visit(parsed)
        result = eval(compile(parsed, '<string>', mode='eval'))
    except Exception as e:
        return f'Error in code execution: {e}', 400

    return str(result)

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test evaluation of safe arithmetic expressions.
- Test rejection of code with function calls, imports, or attribute access.
- Test empty input handling.

## Alternative Solutions

### Use a whitelist of safe commands and parse input accordingly without evaluating code.
**Pros:** More control and less risk than eval-based methods
**Cons:** Less flexible, requires upfront command definition

### Run code in a heavily sandboxed environment like restricted Python interpreters or containers.
**Pros:** Stronger isolation from host system
**Cons:** Higher complexity, overhead


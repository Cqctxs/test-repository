# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used exec() directly on user input, allowing an attacker to execute arbitrary code, leading to a critical security risk. The fix replaces exec() with a safe expression evaluator using Python's ast module to parse and validate the input expression. Only arithmetic operations and specific safe functions are allowed. This prevents execution of arbitrary code while maintaining similar functionality (evaluating simple expressions).

## Security Notes
Never use exec or eval on untrusted input. Using ast parsing to whitelist allowed syntax prevents arbitrary code execution. Further restrictions can be added based on application needs.

## Fixed Code
```py
# Original vulnerable code snippet:
# exec(user_input)

# Secure replacement:
import ast

user_input = get_user_input_somehow()

# Define a set of allowed operations/nodes
allowed_nodes = {
    'Expression', 'BinOp', 'Num', 'Name', 'Load', 'Add', 'Sub', 'Mult', 'Div', 'Mod', 'Pow',
    'UnaryOp', 'USub', 'UAdd', 'Call'
}

# Define allowed functions for calls
allowed_functions = {'abs', 'round', 'min', 'max'}

class SafeEval(ast.NodeVisitor):
    def generic_visit(self, node):
        nodename = type(node).__name__
        if nodename not in allowed_nodes:
            raise ValueError(f"Disallowed expression: {nodename}")
        super().generic_visit(node)

    def visit_Call(self, node):
        if not (isinstance(node.func, ast.Name) and node.func.id in allowed_functions):
            raise ValueError(f"Disallowed function call: {ast.dump(node.func)}")
        self.generic_visit(node)

try:
    tree = ast.parse(user_input, mode='eval')
    SafeEval().visit(tree)
    result = eval(compile(tree, '<string>', 'eval'))
except Exception as e:
    result = None
    # Handle error or log

# Use "result" safely in application

```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test with various harmless expressions to ensure normal operation
- Test with malicious input such as code injection attempts to verify rejection
- Verify error handling behavior on invalid expressions

## Alternative Solutions

### Use a third-party safe expression evaluation library like asteval or numexpr.
**Pros:** Simplifies evaluation of expressions, Provides built-in safety features
**Cons:** Adds external dependencies, May have performance overhead

### Implement a domain-specific language with controlled commands instead of raw code execution.
**Pros:** Full control over allowed operations, Higher security
**Cons:** Requires significant redevelopment, May reduce flexibility


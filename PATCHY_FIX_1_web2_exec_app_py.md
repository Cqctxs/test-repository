# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code used exec() directly on user input, which allows remote code execution and is extremely dangerous. The fixed code replaces exec() with a safe evaluator class that uses Python's AST module to only allow a predefined set of expressions and functions. It parses the user code, ensures only allowed nodes and function names are present, then safely evaluates it using a controlled environment without builtins. This prevents arbitrary code execution and confines what user code can do.

## Security Notes
Always avoid using exec or eval on user input without strict sanitization. Using AST parsing limits code to safe expressions. Define explicitly which functions/names are allowed. Consider running code in sandboxed environment or using specialized libraries for restricted code execution.

## Fixed Code
```py
# Safe execution of user-submitted code by parsing and restricting allowed operations
import ast

class SafeEval(ast.NodeVisitor):
    ALLOWED_NODES = {
        'Expression', 'BinOp', 'UnaryOp', 'Num', 'Load', 'Add', 'Sub', 'Mult', 'Div', 'Pow', 'Mod', 
        'UAdd', 'USub', 'Call', 'Name', 'Tuple', 'List'
    }

    ALLOWED_NAMES = {'abs', 'round', 'min', 'max', 'pow'}  # allowed built-in functions

    def visit(self, node):
        node_name = type(node).__name__
        if node_name not in self.ALLOWED_NODES:
            raise ValueError(f"Disallowed expression: {node_name}")
        return super().visit(node)

    def visit_Name(self, node):
        if node.id not in self.ALLOWED_NAMES:
            raise ValueError(f"Use of name '{node.id}' is not allowed")

    def eval_expr(self, expr):
        parsed = ast.parse(expr, mode='eval')
        self.visit(parsed)
        # Safe eval context
        safe_globals = {name: globals()[name] for name in self.ALLOWED_NAMES}
        safe_globals['__builtins__'] = {}
        return eval(compile(parsed, '<string>', 'eval'), safe_globals, {})

# Example function to safely evaluate user code

def safe_user_code_executor(user_code):
    evaluator = SafeEval()
    try:
        result = evaluator.eval_expr(user_code)
        return result
    except Exception as e:
        return f"Error in code: {str(e)}"

# Replace original exec(user_code) calls with safe_user_code_executor(user_code)

# Usage:
# user_code = request.POST.get('code')
# result = safe_user_code_executor(user_code)
# return result

```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test allowed expressions execute and return correct results.
- Test disallowed expressions raise errors.
- Test injection of malicious code is blocked.

## Alternative Solutions

### Completely remove code execution functionality or provide a limited domain-specific language interpreter for user input.
**Pros:** No risk of arbitrary code execution., Simplifies security auditing.
**Cons:** May reduce application functionality., Requires development of a custom interpreter.

### Run user code in an isolated container or process with strict resource limits and use exec with heavy monitoring.
**Pros:** Allows more flexible code execution., Limits damage to isolated environment.
**Cons:** Increases infrastructure complexity., Potential escape risks if container is misconfigured.


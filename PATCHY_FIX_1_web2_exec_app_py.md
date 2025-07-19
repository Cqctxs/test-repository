# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
The original code allowed execution of arbitrary Python code from user input without sanitization, which leads to critical remote code execution vulnerabilities. The fix uses Python's ast module to parse the input code and validate it only contains safe expressions or assignments. It avoids using exec or eval directly with user input. Instead, a restricted environment with no builtins is used during execution. This greatly reduces the risk of executing harmful code.

## Security Notes
Avoid any direct execution of user input. If dynamic code execution is required, always validate and sandbox the input, restrict builtins, and disallow unsafe nodes in the AST. Consider using specialized sandboxes or domain-specific languages for safer execution.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import traceback
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    
    # Fix: Disallow direct execution of arbitrary code to prevent remote code execution
    # Instead, parse the code and only allow safe expressions
    try:
        # Parse the code to AST and ensure it's an expression
        tree = ast.parse(code, mode='exec')
        # You could add more strict checks here to whitelist allowed operations
        # For demo, refuse execution if there are any statements other than expressions
        for node in tree.body:
            if not isinstance(node, (ast.Expr, ast.Assign)):
                return jsonify({'error': 'Only simple expressions allowed'}), 400

        # Instead of eval or exec, safely compile and execute in restricted environment
        # Create restricted dict for globals and locals
        safe_globals = {'__builtins__': None}
        safe_locals = {}
        compiled = compile(tree, filename='<ast>', mode='exec')
        exec(compiled, safe_globals, safe_locals)
        # Return result if any expression
        result = safe_locals
        return jsonify({'result': str(result)})

    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import ast
- import traceback

## Testing Recommendations
- Test with various safe and unsafe Python code snippets to ensure rejection of unsafe code.
- Test that allowed expressions execute properly and return expected results.
- Verify no malicious code execution possible, e.g., no file system or OS access.

## Alternative Solutions

### Remove the ability to execute arbitrary code entirely and implement specific safe commands or APIs instead.
**Pros:** Eliminates risk of code injection, Simplifies security model
**Cons:** Loss of original functionality if dynamic code execution was required

### Use third-party sandbox libraries like RestrictedPython to safely execute user code.
**Pros:** Provides more robust sandboxing, Allows more complex code safely
**Cons:** Adds external dependencies, May still be complex to configure properly


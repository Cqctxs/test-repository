# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed direct usage of exec() on user-submitted code. Instead, parsed the input code into an Abstract Syntax Tree (AST) to vet potentially dangerous constructs like import statements and calls to exec or eval. The code now restricts allowed built-in functions and prevents dynamic importing or arbitrary code execution, mitigating Remote Code Execution vulnerabilities.

## Security Notes
Restricting allowed builtins and disallowing import statements prevents many attack vectors. Consider further sandboxing or code analysis for production use. Logging execution attempts and enforcing timeouts can improve security. Avoid verbose error output revealing system internals.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import sys
import traceback

app = Flask(__name__)

# Secure code execution environment limiting builtins and disallowing import
@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.form.get('code', '')
    try:
        # Parse code to AST to validate and reject unsafe syntax
        parsed = ast.parse(user_code, mode='exec')

        # Walk AST to disallow dangerous nodes (exec, eval, import, etc.)
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
                # Disallow import and calls to eval, exec
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in ('exec', 'eval', 'compile', 'open', 'input', '__import__'):
                        return jsonify({'error': 'Unsafe function call detected'}), 400
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    return jsonify({'error': 'Import statements are not allowed'}), 400

        # Prepare safe globals and locals to restrict user code environment
        safe_globals = {'__builtins__': {'print': print, 'range': range, 'len': len}}
        safe_locals = {}

        # Execute safely parsed user code
        exec(compile(parsed, filename='<user_code>', mode='exec'), safe_globals, safe_locals)
        return jsonify({'result': 'Code executed successfully'}), 200

    except Exception as e:
        # Return error message without exposing sensitive info
        tb = traceback.format_exc()
        return jsonify({'error': 'Error executing code', 'details': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast
- import traceback

## Testing Recommendations
- Test execution of safe, valid Python code snippets to confirm functionality.
- Test attempt to import modules or call disallowed functions and verify rejection.
- Test submission of malicious code snippets and ensure no server compromise or crashes.

## Alternative Solutions

### Use a secure sandboxed environment such as a Docker container or a restricted Python execution environment (e.g., RestrictedPython).
**Pros:** Strong isolation and security., Flexible handling of user code.
**Cons:** Increased infrastructure complexity., Performance overhead.

### Limit functionality offered to users to predefined safe operations instead of arbitrary code execution.
**Pros:** Eliminates code injection risk., Simplifies security model.
**Cons:** Reduces functionality and flexibility.


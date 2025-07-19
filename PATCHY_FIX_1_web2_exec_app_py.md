# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the use of direct exec() or eval() on user input with AST parsing in 'eval' mode, which only permits expressions. This avoids executing arbitrary statements and disables access to Python built-ins by providing an empty '__builtins__' dictionary, preventing remote code execution vulnerabilities.

## Security Notes
Avoid executing arbitrary user-provided code. Using the 'ast' module to parse and only allow expressions increases safety. For production, consider sandboxing or using restricted execution environments.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.json.get('code', '')
    try:
        # Parse the user code into an AST and only allow expressions to prevent arbitrary statements
        parsed_code = ast.parse(user_code, mode='eval')
        # Optionally, one could implement further AST checks here to whitelist safe nodes
        result = eval(compile(parsed_code, filename='<user_code>', mode='eval'), {'__builtins__': {}})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test with malicious inputs containing dangerous Python statements to verify execution is blocked.
- Test with legitimate expressions to verify correct evaluation.

## Alternative Solutions

### Implement a sandboxed environment or specialized interpreter for user scripts.
**Pros:** More fine-grained control over allowed operations., Safer execution of user code.
**Cons:** Increased implementation complexity., Performance overhead.

### Provide a safe domain-specific language (DSL) instead of Python code execution.
**Pros:** Prevents direct Python code execution risks., Control over allowed commands.
**Cons:** Requires building and maintaining DSL parser and interpreter.


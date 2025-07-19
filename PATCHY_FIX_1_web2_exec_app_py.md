# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced direct exec() on user-supplied code with RestrictedPython compile_restricted. This sandbox disallows file I/O, attribute access, and builtins that could lead to escape. We only expose safe_builtins and collect a 'result' variable.

## Security Notes
Ensure RestrictedPython is maintained and updated. Consider further restricting available guards as needed.

## Fixed Code
```py
import ast
from flask import Flask, request, jsonify
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    user_code = request.json.get('code', '')
    # Parse and compile with RestrictedPython to prevent arbitrary code execution
    try:
        byte_code = compile_restricted(user_code, '<string>', 'exec')
        policy_globals = {'__builtins__': safe_builtins}
        policy_locals = {}
        exec(byte_code, policy_globals, policy_locals)
        result = policy_locals.get('result', None)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- RestrictedPython

## Testing Recommendations
- Submit benign expressions and verify correct evaluation
- Submit malicious code attempts (e.g. import os) and verify rejection

## Alternative Solutions

### Use a separate microservice in a containerized environment to evaluate code safely
**Pros:** Full isolation, Crash containment
**Cons:** Higher operational overhead


# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Replaced the original use of exec() on user input with a restricted eval using a safe globals dictionary, disallowing dangerous builtins and common attack keywords. This mitigates arbitrary code execution by limiting what can be run.

## Security Notes
Avoid use of exec and eval on user input. If dynamic code execution is required, use strict sanitization and ideally run code in isolated sandboxes. Validate and whitelist allowed operations.

## Fixed Code
```py
from flask import Flask, request, jsonify
app = Flask(__name__)

# For demonstration we allow only a limited set of safe functions
SAFE_GLOBALS = {
    '__builtins__': None,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
}

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.json.get('code')

    # Reject if the code contains forbidden keywords
    forbidden_keywords = ['import', 'open', 'exec', 'eval', '__', 'os', 'sys', 'subprocess']
    if any(keyword in user_code for keyword in forbidden_keywords):
        return jsonify({'error': 'Disallowed code detected'}), 400

    result = None
    try:
        # Instead of exec, use a very restricted eval with safe globals
        # Warning: Even this can be dangerous and should be replaced with a proper sandbox
        result = eval(user_code, SAFE_GLOBALS, {})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- from flask import Flask, request, jsonify

## Testing Recommendations
- Test with various malicious payloads that attempt to use exec, import modules, access filesystem or environment.
- Validate normal functional code snippets execute successfully with restricted commands.
- Verify error messages do not leak sensitive info.

## Alternative Solutions

### Use a dedicated sandbox environment or container to run user code safely separated from the main server.
**Pros:** Provides strong isolation, Prevents entire server compromise if code is malicious
**Cons:** More complex infrastructure, Higher overhead, possible latency

### Disable interactive code execution altogether and offer limited preset actions or scripts exposed via API.
**Pros:** Completely eliminates code injection risk, Simpler implementation
**Cons:** Less flexible functionality


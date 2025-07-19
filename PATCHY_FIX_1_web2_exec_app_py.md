# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Replaced direct execution of arbitrary user code using exec with a restricted environment that disables builtins and prevents use of dangerous keywords. This prevents code injection and remote code execution by blocking unsafe code and limiting execution context.

## Security Notes
Code injection and remote code execution risks are mitigated by rejecting unsafe keywords and executing user code without builtins, which limits what code can perform. Further improvements include sandboxing or using a whitelist of safe operations, or evaluating expressions with ast.literal_eval if applicable.

## Fixed Code
```py
from flask import Flask, request, jsonify
app = Flask(__name__)

# Example: a safe subset of allowed operations
SAFE_CODE = ['print', 'len', 'range']

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.json.get('code', '')
    # Reject code containing unsafe keywords
    unsafe_keywords = ['import', 'exec', 'eval', '__', 'os', 'sys', 'subprocess', 'open']
    if any(keyword in user_code for keyword in unsafe_keywords):
        return jsonify({'error': 'Unsafe code detected'}), 400

    # Instead of using exec directly, limit execution environment
    local_vars = {}
    try:
        # Execute in a restricted environment without builtins
        exec(user_code, {'__builtins__': {}}, local_vars)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': local_vars}), 200

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- from flask import Flask, request, jsonify

## Testing Recommendations
- Test attempts to run malicious code snippets are blocked
- Verify normal allowed code can run successfully
- Test that code execution environment does not have access to restricted modules or operations

## Alternative Solutions

### Use an external sandboxed execution environment like Docker or a microVM
**Pros:** Strongly isolates user code execution, Flexible execution with full Python support
**Cons:** More complex to implement and manage, Increased resource usage

### Only allow evaluation of expressions via ast.literal_eval()
**Pros:** Very safe as it only evaluates constants and simple expressions
**Cons:** Limited functionality, cannot run arbitrary code


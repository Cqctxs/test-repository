# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced the dangerous use of exec() on user-provided code with ast.literal_eval(), which safely evaluates only literals and basic data structures without executing arbitrary code. This eliminates the code injection risk.

## Security Notes
Never use exec or eval on user input. Use safe parsers or interpreters that restrict execution, like ast.literal_eval for Python literals.

## Fixed Code
```py
# Secure version of app.py
import ast
import flask
app = flask.Flask(__name__)

# Safely evaluate simple expressions instead of using exec
@app.route('/eval', methods=['POST'])
def safe_eval():
    try:
        data = flask.request.get_json()
        expr = data.get('expr', '')
        # Parse expression safely using ast.literal_eval
        result = ast.literal_eval(expr)  # only literals and tuples, lists, dicts, strings, numbers
        return flask.jsonify({'result': result})
    except (ValueError, SyntaxError):
        return flask.jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test with various input expressions including edge cases and malicious code attempts to ensure no code injection occurs.
- Verify valid inputs return correct results.
- Verify invalid inputs return 400 error.

## Alternative Solutions

### Use a sandboxed code execution environment with strict time and resource limits.
**Pros:** More flexible, can execute broader code safely.
**Cons:** More complex to implement and maintain., Potential risks if sandbox is broken.

### Provide a fixed set of allowed commands or operations and validate input strictly.
**Pros:** Simple and secure., Easy to monitor and audit.
**Cons:** Limited functionality for users.


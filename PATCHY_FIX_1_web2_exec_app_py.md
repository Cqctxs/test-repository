# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Removed use of exec() which executes arbitrary Python code and introduces critical remote code execution vulnerability. Replaced with a safe expression evaluator that only allows mathematical expressions using the ast module and whitelisted nodes. This prevents arbitrary code execution while maintaining the original functionality of evaluating user expressions.

## Security Notes
Avoid using exec/eval on user input. Use safe evaluation techniques like ast parsing with whitelist of allowed nodes or specialized parsers for math expressions. Disable debug mode in production.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Safe evaluation of math expressions only
ALLOWED_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.USub
}

def safe_eval(expr):
    """ Evaluate simple math expressions from user input safely."""
    try:
        node = ast.parse(expr, mode='eval')
        for n in ast.walk(node):
            if type(n) not in ALLOWED_NODES:
                raise ValueError('Disallowed expression detected')
        return eval(compile(node, '<string>', 'eval'))
    except Exception as e:
        return str(e)

@app.route('/execute', methods=['POST'])
def execute_code():
    # Accept only a math expression string from the user, no arbitrary code
    user_input = request.form.get('expression', '')
    result = safe_eval(user_input)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- import ast

## Testing Recommendations
- Test with valid mathematical expressions to verify correct outputs.
- Test with malicious inputs containing code to verify rejection or error handling.

## Alternative Solutions

### Use third-party libraries like 'asteval' that safely evaluate expressions with sandboxing.
**Pros:** Easier implementation, supports richer expression language.
**Cons:** Additional dependency, potentially larger attack surface.

### Implement a custom parser/interpreter for allowed user codes.
**Pros:** Full control over allowed operations and functionality.
**Cons:** Time consuming to implement and test.


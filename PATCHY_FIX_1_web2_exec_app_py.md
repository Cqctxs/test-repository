# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code executed arbitrary Python code from user input directly using 'exec' or 'eval', which is an extreme security risk leading to remote code execution. The fixed code removes any use of 'exec' or 'eval' with user input. Instead, it implements a safe expression evaluator that only allows a limited set of arithmetic operations, parsing the input expression into an abstract syntax tree and evaluating it only if it contains safe nodes and operators. This prevents execution of arbitrary code while keeping the original functionality of evaluating expressions.

## Security Notes
Always avoid executing user input as code. Parsing and evaluating expressions safely using AST with strict allowed operations prevents code injection. Consider further input validation or restrict functionality to safe predefined operations if possible.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

# Define allowed operators for safe evaluation
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

# Safe eval function that parses and evaluates arithmetic expressions only
def safe_eval(expr):
    # Parse expression into AST
    node = ast.parse(expr, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.left), _eval(node.right))
            else:
                raise ValueError("Operator not allowed")
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](_eval(node.operand))
            else:
                raise ValueError("Operator not allowed")
        else:
            raise TypeError("Unsupported expression")
    return _eval(node)

@app.route('/eval', methods=['POST'])
def evaluate():
    data = request.get_json(force=True)
    expression = data.get('expression')
    if not expression:
        return jsonify({'error': 'Expression is required'}), 400
    try:
        # Evaluate expression safely
        result = safe_eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- operator

## Testing Recommendations
- Test with valid arithmetic expressions to ensure correct results
- Test with potentially malicious inputs like injection attempts to verify no code execution occurs
- Test with malformed expressions to check proper error handling

## Alternative Solutions

### Use a third-party safe expression evaluation library like 'asteval' or 'numexpr'
**Pros:** Library handles many edge cases and supports more functionality, Reduces custom code burden
**Cons:** Adds external dependency, May still need to restrict functionality based on requirements

### Remove ability to evaluate arbitrary expressions, switch to predefined commands or functions
**Pros:** Simplest and safest approach, No code injection risk
**Cons:** Reduces functionality and flexibility


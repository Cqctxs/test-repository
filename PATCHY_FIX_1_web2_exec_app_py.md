# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code executed arbitrary code from user input unsafely risking remote code execution. We replaced the unsafe eval/exec with a safe literal expression evaluator using the ast module. This limits execution to safe mathematical operations, preventing code injection attacks.

## Security Notes
Never use exec or eval on user input. Use parsers and controlled evaluation. Validate or strictly limit input. SafeEval only executes arithmetic expressions, rejecting malicious payloads.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

# Safe eval implementation using ast to parse and evaluate expressions
class SafeEval(ast.NodeVisitor):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg
    }

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type}")
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")
        else:
            raise ValueError(f"Unsupported expression: {type(node)}")

@app.route('/eval')
def safe_eval():
    expression = request.args.get('expr', '')
    try:
        # Parse the expression into AST
        parsed_expr = ast.parse(expression, mode='eval')
        # Evaluate using safe visitor
        evaluator = SafeEval()
        result = evaluator.visit(parsed_expr)
    except Exception as e:
        return jsonify({'error': 'Invalid expression', 'details': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

```

## Additional Dependencies
- ast
- operator

## Testing Recommendations
- Test valid math expressions to confirm correct evaluation
- Test malicious inputs like '__import__("os").system("rm -rf /")' and confirm rejection
- Test edge cases for allowed operations

## Alternative Solutions

### Use a sandboxed environment for executing user-supplied code using third-party secure sandbox libraries
**Pros:** Allows more complex computations safely
**Cons:** More complex setup, overhead, external dependencies

### Limit user input to predefined commands or expressions rather than arbitrary code
**Pros:** Simpler and secure
**Cons:** Less flexible for users


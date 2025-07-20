import ast

# Define a safe evaluator by whitelisting AST nodes
class SafeEvaluator(ast.NodeVisitor):
    SAFE_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Num, ast.Str, ast.NameConstant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.Load, ast.Mod,
    }

    def visit(self, node):
        if type(node) not in self.SAFE_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        return super().visit(node)

    def eval(self, expr: str):
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')
        # Validate AST
        self.visit(tree)
        # Compile and evaluate safely
        code = compile(tree, filename='<safe>', mode='eval')
        return eval(code, {'__builtins__': {}})


def calculate_expression(user_input):
    """
    Safely evaluate a mathematical expression provided by the user.
    """
    try:
        evaluator = SafeEvaluator()
        result = evaluator.eval(user_input)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}

# Example usage in a web framework handler
# user_input = request.args.get('expr')
# response = calculate_expression(user_input)

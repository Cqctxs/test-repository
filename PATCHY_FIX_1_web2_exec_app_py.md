# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
The original code executed user-protected input directly with exec(), which allows arbitrary code execution.
This fix replaces exec() with an AST parsing method that walks the syntax tree to disallow unsafe statements like import, exec call, and uncontrolled function calls.
Only specific safe built-in functions defined in SAFE_NAMES can be called.
This limits code execution to a tightly controlled subset, preventing remote code execution.

## Security Notes
- Avoid using exec() or eval() with user input.
- Use parsing methods such as ast to validate syntax and disallow risky nodes.
- Define a whitelist of allowed functions and disallow imports.
- Consider sandboxing or containerizing code execution if needed for isolation.

## Fixed Code
```py
import ast
import sys
import traceback

# Define a safe list of allowed names and functions for execution
SAFE_NAMES = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    # Add other safe built-ins as needed
}


def safe_exec(user_code):
    """
    Safely execute user-provided Python code by parsing and restricting what can be run.
    This function prevents arbitrary code execution vulnerabilities.
    """
    try:
        # Parse the code to an AST tree
        tree = ast.parse(user_code, mode='exec')

        # Walk the AST tree to ensure it contains only safe nodes
        for node in ast.walk(tree):
            if isinstance(node, (ast.Exec, ast.Import, ast.ImportFrom, ast.Call)):
                # Disallow exec calls, imports, and function calls except to safe functions
                if isinstance(node, ast.Call):
                    # Allow calls only to functions in SAFE_NAMES
                    if not (isinstance(node.func, ast.Name) and node.func.id in SAFE_NAMES):
                        raise ValueError("Use of unsafe function or call detected")
                else:
                    raise ValueError("Disallowed node type in code")

        # Compile and execute the safe code in a limited environment
        exec(compile(tree, filename='<user_code>', mode='exec'), {'__builtins__': SAFE_NAMES}, {})

    except Exception as e:
        # Log the error safely without exposing internals
        sys.stderr.write(f"Error during code execution: {e}\n")
        traceback.print_exc()


# Example usage:
# user_input = request.form.get('code')  # For a web app
# safe_exec(user_input)

```

## Additional Dependencies
- import ast
- import sys
- import traceback

## Testing Recommendations
- Test execution of allowed code snippets.
- Test attempts to use disallowed keywords or calls (import, exec, system calls).
- Verify no arbitrary system commands can be executed.

## Alternative Solutions

### Use a sandboxed execution environment like RestrictedPython or a separate container/job runner.
**Pros:** Strong security isolation, Prebuilt filters for unsafe constructs
**Cons:** More complex setup, Requires dependency and environment management

### Implement a domain-specific language or template system instead of Python code execution.
**Pros:** Eliminates arbitrary code execution risk, Simplifies permissions management
**Cons:** Limited expressiveness, Potentially requires more development effort


# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Added session-based authentication and authorization checks to verify that only admins can update account balances. Implemented input validation and sanitization. Used prepared statements with PDO to securely update database and prevent SQL injection. Added appropriate HTTP response codes and error handling.

## Security Notes
Always authenticate and authorize before performing critical operations. Sanitize and validate all user inputs. Use prepared statements to avoid SQL injection. Configure session securely and use HTTPS in production.

## Fixed Code
```php
<?php
session_start();

// Check if user is authenticated and authorized
// Assume user roles stored in session as 'user_role'

if (!isset($_SESSION['user_role']) || $_SESSION['user_role'] != 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden']);
    exit();
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input || !isset($input['account']) || !isset($input['amount'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit();
}

$account = $input['account'];
$amount = $input['amount'];

// Validate input types
if (!is_string($account) || !is_numeric($amount)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input types']);
    exit();
}

// Sanitize inputs
$account = htmlspecialchars($account, ENT_QUOTES, 'UTF-8');
$amount = floatval($amount);

// Connect to database securely
$pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'password');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Use prepared statements to prevent SQL Injection
$stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amount WHERE account_number = :account');
$stmt->bindParam(':amount', $amount, PDO::PARAM_STR);
$stmt->bindParam(':account', $account, PDO::PARAM_STR);
$stmt->execute();

echo json_encode(['success' => true]);
?>
```

## Additional Dependencies
None

## Testing Recommendations
- Test unauthorized requests are rejected with 403.
- Test valid requests modify balances correctly.
- Test SQL Injection attempts fail.

## Alternative Solutions

### Implement token-based authentication (e.g., JWT) in PHP gateway instead of session.
**Pros:** Stateless authentication., Easier scaling.
**Cons:** Require clients to store/refresh tokens securely.


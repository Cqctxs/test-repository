# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Added session-based authentication to restrict financial operations to logged-in users. The sender is determined from the authenticated user session, and all inputs for recipient and amount are sanitized and validated using regex and PHP built-in filters. Unauthorized or malformed requests are rejected with appropriate HTTP codes.

## Security Notes
Always require authentication for sensitive API endpoints. Validate all inputs with allowlists or type validation. Use HTTPS to protect session cookie confidentiality. Store passwords hashed in real applications.

## Fixed Code
```php
<?php
session_start();

// Simple user database with balances
$users = array(
    'Eatingfood' => array('password' => 'somehashedpassword', 'balance' => 1000),
    // ...
);

// Authentication check function
function authenticate() {
    if (!isset($_SESSION['username'])) {
        http_response_code(401);
        echo 'Authentication required';
        exit;
    }
}

// Input validation function
function validate_input($data) {
    // Using allowlist for usernames
    if (!preg_match('/^[a-zA-Z0-9]{3,20}$/', $data)) {
        return false;
    }
    return $data;
}

// Sanitize and validate POST parameters
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    authenticate();

    $sender = $_SESSION['username']; // Trust session user
    $recipient = isset($_POST['recipient']) ? validate_input($_POST['recipient']) : null;
    $amount = isset($_POST['amount']) ? filter_var($_POST['amount'], FILTER_VALIDATE_FLOAT) : null;

    if (!$recipient || !$amount || $amount <= 0) {
        http_response_code(400);
        echo 'Invalid input parameters';
        exit;
    }

    global $users;

    if (!isset($users[$recipient]) || !isset($users[$sender])) {
        http_response_code(400);
        echo 'Sender or recipient not found';
        exit;
    }

    if ($users[$sender]['balance'] < $amount) {
        http_response_code(400);
        echo 'Insufficient funds';
        exit;
    }

    // Perform transfer
    $users[$sender]['balance'] -= $amount;
    $users[$recipient]['balance'] += $amount;

    echo 'Transfer successful';
} else {
    http_response_code(405);
    echo 'Method not allowed';
}

// Add login endpoint for illustration
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] == 'login') {
    $username = isset($_POST['username']) ? validate_input($_POST['username']) : null;
    $password = isset($_POST['password']) ? $_POST['password'] : null;

    global $users;
    if ($username && $password && isset($users[$username]) && $users[$username]['password'] === $password) {
        $_SESSION['username'] = $username;
        echo 'Login successful';
    } else {
        http_response_code(401);
        echo 'Invalid credentials';
    }
}
?>
```

## Additional Dependencies
None

## Testing Recommendations
- Test login and session establishment.
- Test transfer with valid login and reject when not logged in.
- Test input validation with invalid usernames and amounts.

## Alternative Solutions

### Use token-based API authentication (e.g., JWT) with middleware validation.
**Pros:** More flexible for stateless API clients
**Cons:** Requires token issuance and revocation logic


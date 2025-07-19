# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Added session-based authentication check to ensure only authenticated users can modify account balances. Inputs from POST request are validated for presence and type. Sender's balance is checked before transferring funds to prevent overdraft. Recipient existence is also validated. This mitigates unauthorized fund transfers and input tampering.

## Security Notes
Implement proper authentication, session management, and verify authorization on all critical operations in PHP web apps. Avoid trusting POST data without validation. Always check and sanitize inputs before database or business logic operations.

## Fixed Code
```php
<?php
session_start();

// Dummy user data and balances (in real app use DB and authentication)
$users = array(
    'Eatingfood' => array('balance' => 1000),
    'Recipient' => array('balance' => 500)
);

// Require authentication
if (!isset($_SESSION['username'])) {
    http_response_code(401);
    echo json_encode(array('error' => 'Authentication required'));
    exit;
}

// Check method
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $sender = $_SESSION['username'];
    $recipient = $_POST['recipient'] ?? '';
    $amount = floatval($_POST['amount'] ?? 0);

    // Basic input validation
    if (empty($recipient) || $amount <= 0) {
        http_response_code(400);
        echo json_encode(array('error' => 'Invalid recipient or amount'));
        exit;
    }

    // Check if sender has enough balance
    if (!isset($users[$sender]) || $users[$sender]['balance'] < $amount) {
        http_response_code(400);
        echo json_encode(array('error' => 'Insufficient funds'));
        exit;
    }

    // Check recipient exists
    if (!isset($users[$recipient])) {
        http_response_code(400);
        echo json_encode(array('error' => 'Recipient not found'));
        exit;
    }

    // Perform transfer
    $users[$sender]['balance'] -= $amount;
    $users[$recipient]['balance'] += $amount;

    // Respond success
    echo json_encode(array('message' => 'Transfer successful', 'sender_balance' => $users[$sender]['balance']));
    exit;
}

?>
```

## Additional Dependencies
None

## Testing Recommendations
- Test POST request without login fails with 401.
- Test valid authenticated POST request performs transfer correctly.
- Test invalid inputs like negative amount or unknown recipient get 400 errors.

## Alternative Solutions

### Use OAuth or JWT tokens for API authentication instead of sessions.
**Pros:** Better for REST APIs, Stateless authentication
**Cons:** Requires token management and validation


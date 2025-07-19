# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
The original PHP API lacked authentication and authorization checks, allowing anyone to submit POST requests that directly manipulated account balances, causing unauthorized fund transfers. The fix implements session-based authentication checking, sanitizes and validates inputs, verifies sender identity from session, ensures recipient exists, and performs balance update within a transaction using prepared statements to prevent SQL injection and race conditions. This ensures only authorized users can manipulate their funds and input is validated to prevent tampering or injection.

## Security Notes
Ensure session management with secure cookies and HTTPS. Use prepared statements for all SQL queries to protect against SQL Injection. Validate and sanitize all inputs. Use transactions to maintain database integrity during balance updates.

## Fixed Code
```php
<?php
session_start();

// Check if user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

// Connect to database using PDO with prepared statements
try {
    $pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'password', [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Validate and sanitize inputs
$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
$recipient = filter_input(INPUT_POST, 'recipient', FILTER_SANITIZE_STRING);
if ($amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}
if (!$recipient || strlen($recipient) > 100) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid recipient']);
    exit;
}

// Check authorization: make sure logged in user is the sender
$sender_id = $_SESSION['user_id'];

// Ensure recipient exists
$stmt = $pdo->prepare('SELECT id FROM users WHERE username = ?');
$stmt->execute([$recipient]);
$recipient_data = $stmt->fetch(PDO::FETCH_ASSOC);
if (!$recipient_data) {
    http_response_code(400);
    echo json_encode(['error' => 'Recipient not found']);
    exit;
}
$recipient_id = $recipient_data['id'];

// Begin transaction to safely update balances
try {
    $pdo->beginTransaction();
    
    // Check sender balance
    $stmt = $pdo->prepare('SELECT balance FROM accounts WHERE user_id = ? FOR UPDATE');
    $stmt->execute([$sender_id]);
    $sender_account = $stmt->fetch(PDO::FETCH_ASSOC);
    if (!$sender_account || $sender_account['balance'] < $amount) {
        $pdo->rollBack();
        http_response_code(400);
        echo json_encode(['error' => 'Insufficient funds']);
        exit;
    }

    // Deduct from sender
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance - ? WHERE user_id = ?');
    $stmt->execute([$amount, $sender_id]);

    // Add to recipient
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + ? WHERE user_id = ?');
    $stmt->execute([$amount, $recipient_id]);

    $pdo->commit();
    echo json_encode(['message' => 'Transfer successful']);
} catch (Exception $e) {
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error' => 'Transfer failed']);
}

?>
```

## Additional Dependencies
None

## Testing Recommendations
- Test unauthorized requests are rejected.
- Test transfers with valid and invalid recipients and amounts.
- Test concurrent transfers to verify transaction isolation.

## Alternative Solutions

### Implement token-based authentication (e.g., JWT) for API access control.
**Pros:** Scalable for APIs, Stateless authentication
**Cons:** Token management complexity, Needs secure transmission and storage


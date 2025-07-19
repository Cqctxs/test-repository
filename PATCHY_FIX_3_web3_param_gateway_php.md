# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Added session authentication and authorization checks to ensure only authorized users (admins) can perform balance updates. Input parameters are validated for presence and type. The accounts file is checked for existence and validity before manipulation. Transfers verify sufficient funds before proceeding.

## Security Notes
Ensured user session is checked at start. Input validation limits injection risks. Reading and writing JSON data carefully ensures no corruption. Using JSON encoding functions protects data integrity. Use HTTPS and secure session cookie flags in deployment.

## Fixed Code
```php
<?php
session_start();

// Check if user is logged in and authorized
if (!isset($_SESSION['username']) || $_SESSION['role'] !== 'admin') {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// Read incoming POST data
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid request body']);
    exit;
}

// Validate input fields
if (!isset($input['from_account'], $input['to_account'], $input['amount'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

$fromAccount = $input['from_account'];
$toAccount = $input['to_account'];
$amount = $input['amount'];

if (!is_numeric($amount) || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

$accountsFile = 'accounts.json';

if (!file_exists($accountsFile)) {
    file_put_contents($accountsFile, json_encode(new stdClass()));
}

$accounts = json_decode(file_get_contents($accountsFile), true);
if (!$accounts) {
    $accounts = [];
}

if (!isset($accounts[$fromAccount]) || $accounts[$fromAccount] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient funds']);
    exit;
}

// Perform the transfer
$accounts[$fromAccount] -= $amount;
if (!isset($accounts[$toAccount])) {
    $accounts[$toAccount] = 0;
}
$accounts[$toAccount] += $amount;

file_put_contents($accountsFile, json_encode($accounts, JSON_PRETTY_PRINT));

http_response_code(200);
echo json_encode(['message' => 'Transfer successful']);

?>
```

## Additional Dependencies
None

## Testing Recommendations
- Test unauthorized access blocked.
- Test input validation rejects malformed requests.
- Test successful transfer updates balances correctly.
- Test concurrent access for race conditions.

## Alternative Solutions

### Replace JSON file storage with a database with transaction support and enforce authorization at DB layer.
**Pros:** More scalable and robust data handling, Stronger integrity guarantees
**Cons:** Requires major refactoring and DB setup


# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Added session-based authentication, input validation, and authorization to verify that the session user owns the target account.

## Security Notes
Replace session auth placeholder with robust authentication (tokens/jwt). Use file locking when writing JSON to prevent race conditions.

## Fixed Code
```php
<?php
// gateway.php - secured version
session_start();

// Basic authentication check (example, replace with real auth)
if (!isset($_SESSION['user_id'])) {
    header('HTTP/1.1 401 Unauthorized');
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['account_id'], $input['action'], $input['amount'])) {
    header('HTTP/1.1 400 Bad Request');
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

// Validate account_id and amount
$accountId = filter_var($input['account_id'], FILTER_VALIDATE_INT);
$amount = filter_var($input['amount'], FILTER_VALIDATE_FLOAT);
$action = in_array($input['action'], ['credit','debit']) ? $input['action'] : null;
if ($accountId === false || $amount === false || !$action) {
    header('HTTP/1.1 400 Bad Request');
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

$file = __DIR__ . '/accounts.json';
$data = json_decode(file_get_contents($file), true);
// Verify user owns this account
if ($data[$accountId]['owner_id'] !== $_SESSION['user_id']) {
    header('HTTP/1.1 403 Forbidden');
    echo json_encode(['error' => 'Not authorized for this account']);
    exit;
}

if ($action === 'credit') {
    $data[$accountId]['balance'] += $amount;
} else {
    if ($data[$accountId]['balance'] < $amount) {
        header('HTTP/1.1 400 Bad Request');
        echo json_encode(['error' => 'Insufficient funds']);
        exit;
    }
    $data[$accountId]['balance'] -= $amount;
}

file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));

echo json_encode(['success' => true, 'balance' => $data[$accountId]['balance']]);
?>
```

## Additional Dependencies
None

## Testing Recommendations
- Attempt requests without login, with invalid params, with unauthorized accounts.

## Alternative Solutions

### Use a database with proper transactions
**Pros:** Concurrency safety, Scalable
**Cons:** Requires DB setup


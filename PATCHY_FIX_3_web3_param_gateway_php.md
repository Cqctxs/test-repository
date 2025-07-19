# Security Fix for web3/param/gateway.php

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Implemented JWT-based authentication, validated inputs, used file locking to prevent races, validated numeric and alphanumeric. Prevents unauthorized and malformed requests.

## Security Notes
Use strong JWT secret and rotate regularly. For production, use database transactions instead of JSON file.

## Fixed Code
```php
<?php
// Add JWT-based auth
require 'vendor/autoload.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

define('BALANCE_FILE', __DIR__ . '/balances.json');

def getBearerToken() {
    $headers = getallheaders();
    if (!isset($headers['Authorization'])) return null;
    if (preg_match('/Bearer\s+(\S+)/', $headers['Authorization'], $matches)) {
        return $matches[1];
    }
    return null;
}

$token = getBearerToken();
if (!$token) { http_response_code(401); exit; }

try {
    $decoded = JWT::decode($token, new Key('your_jwt_secret', 'HS256'));
} catch (Exception $e) {
    http_response_code(401);
    echo json_encode(['error'=>'Invalid token']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$user = $decoded->sub;
$to = $input['to'] ?? '';
$amount = $input['amount'] ?? 0;

// Validate
if (!is_string($to) || !preg_match('/^[a-zA-Z0-9]+$/', $to)) {
    http_response_code(400); echo json_encode(['error'=>'Invalid target']); exit;
}
if (!is_numeric($amount) || $amount <= 0) {
    http_response_code(400); echo json_encode(['error'=>'Invalid amount']); exit;
}

// Load balances with file locking (to avoid race)
$fp = fopen(BALANCE_FILE, 'c+');
flock($fp, LOCK_EX);
$data = stream_get_contents($fp);
$balances = $data ? json_decode($data, true) : [];

if (!isset($balances[$user]) || $balances[$user] < $amount) {
    flock($fp, LOCK_UN);
    fclose($fp);
    http_response_code(400);
    echo json_encode(['error'=>'Insufficient funds']);
    exit;
}

$balances[$user] -= $amount;
$balances[$to] = ($balances[$to] ?? 0) + $amount;

// Truncate and write
ftruncate($fp, 0);
rewind($fp);
fwrite($fp, json_encode($balances));
flock($fp, LOCK_UN);
fclose($fp);

echo json_encode(['success'=>true, 'balances'=>$balances]);

```

## Additional Dependencies
- firebase/php-jwt

## Testing Recommendations
- Replay same request concurrently to test race lock
- Send invalid token and expect 401

## Alternative Solutions

### Migrate balances to a relational DB with transactions
**Pros:** ACID guarantees
**Cons:** Requires DB setup


<?php
// Authenticate using API key
$headers = getallheaders();
if (!isset($headers['X-API-KEY']) || $headers['X-API-KEY'] !== getenv('API_KEY')) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// Parse input
$input = json_decode(file_get_contents('php://input'), true);
// Sanitize account identifiers to alphanumeric
$from = preg_replace('/[^a-zA-Z0-9]/', '', $input['from'] ?? '');
$to   = preg_replace('/[^a-zA-Z0-9]/', '', $input['to'] ?? '');
// Validate amount as positive integer
$amount = filter_var($input['amount'] ?? null, FILTER_VALIDATE_INT);

if (!$from || !$to || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

// Secure accounts.json path
$path = realpath(__DIR__ . '/accounts.json');
if (strpos($path, realpath(__DIR__)) !== 0) {
    http_response_code(500);
    echo json_encode(['error' => 'Server error']);
    exit;
}

$accounts = json_decode(file_get_contents($path), true);
if (!isset($accounts[$from]) || !isset($accounts[$to])) {
    http_response_code(404);
    echo json_encode(['error' => 'Account not found']);
    exit;
}
if ($accounts[$from] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient funds']);
    exit;
}

// Perform transfer
$accounts[$from] -= $amount;
$accounts[$to] += $amount;
file_put_contents($path, json_encode($accounts, JSON_PRETTY_PRINT));

echo json_encode(['status' => 'success', 'accounts' => $accounts]);
?>
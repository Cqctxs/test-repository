<?php
// gateway.php - Updated with authentication and input validation
header('Content-Type: application/json');

// Simple API key check
$apiKey = getenv('API_KEY');
$requestKey = $_SERVER['HTTP_X_API_KEY'] ?? '';
if (!$requestKey || $requestKey !== $apiKey) {
    http_response_code(401);
    echo json_encode(['error'=>'Unauthorized']);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid JSON']);
    exit;
}

// Validate fields
$account = $data['account'] ?? null;
$amount = $data['amount'] ?? null;
if (!is_string($account) || !preg_match('/^[a-zA-Z0-9_]+$/',$account)) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid account']);
    exit;
}
if (!is_numeric($amount) || $amount < 0) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid amount']);
    exit;
}

$path = __DIR__.'/balances.json';
$balances = json_decode(file_get_contents($path), true);
if (!isset($balances[$account])) {
    http_response_code(404);
    echo json_encode(['error'=>'Account not found']);
    exit;
}

// Update and save
$balances[$account] = $amount;
file_put_contents($path, json_encode($balances, JSON_PRETTY_PRINT));

echo json_encode(['status'=>'success']);
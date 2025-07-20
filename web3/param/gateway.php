<?php
session_start();

// Simple token-based authentication for demonstration
$valid_api_token = 'REPLACE_WITH_SECURE_TOKEN';

if ($_SERVER['HTTP_AUTHORIZATION'] !== 'Bearer ' . $valid_api_token) {
    header('HTTP/1.1 401 Unauthorized');
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['account']) || !isset($input['amount'])) {
    header('HTTP/1.1 400 Bad Request');
    echo json_encode(['error' => 'Missing parameters']);
    exit;
}

$account = preg_replace('/[^a-zA-Z0-9_\-]/', '', $input['account']);
$amount = filter_var($input['amount'], FILTER_VALIDATE_FLOAT);
if ($amount === false) {
    header('HTTP/1.1 400 Bad Request');
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

$file = __DIR__ . '/accounts.json';
$data = json_decode(file_get_contents($file), true);
if (!array_key_exists($account, $data)) {
    header('HTTP/1.1 404 Not Found');
    echo json_encode(['error' => 'Account not found']);
    exit;
}

// Perform balance update
$data[$account]['balance'] += $amount;
file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));

header('Content-Type: application/json');
echo json_encode(['status' => 'success', 'balance' => $data[$account]['balance']]);
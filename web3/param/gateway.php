<?php
session_start();
header('Content-Type: application/json');

// Authentication check
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['from'], $input['to'], $input['amount'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

// Validate and sanitize inputs
$from   = filter_var($input['from'], FILTER_SANITIZE_STRING);
$to     = filter_var($input['to'], FILTER_SANITIZE_STRING);
$amount = filter_var($input['amount'], FILTER_VALIDATE_FLOAT);

if ($amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

$balances = json_decode(file_get_contents('balances.json'), true);

// Authorization: only account owner can transfer
if ($_SESSION['user_id'] !== $from) {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden']);
    exit;
}

// Business logic checks
if (!isset($balances[$from]) || !isset($balances[$to]) || $balances[$from] < $amount) {
    http_response_code(400);
    echo json_encode(['error' => 'Insufficient funds or invalid account']);
    exit;
}

$balances[$from] -= $amount;
$balances[$to]   += $amount;
file_put_contents('balances.json', json_encode($balances, JSON_PRETTY_PRINT));

echo json_encode(['status' => 'success']);
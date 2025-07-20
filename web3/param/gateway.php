<?php
session_start();
header('Content-Type: application/json');

// Check authentication
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Not authenticated']);
    exit;
}

// Decode and validate input
$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['balance'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing balance field']);
    exit;
}

// Ensure user only updates own account
$user_id = (int) $_SESSION['user_id'];
$balance = filter_var($input['balance'], FILTER_VALIDATE_FLOAT);
if ($balance === false || $balance < 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid balance']);
    exit;
}

$accountsFile = __DIR__ . '/accounts.json';
$accounts = json_decode(file_get_contents($accountsFile), true);
if (!isset($accounts[$user_id])) {
    http_response_code(404);
    echo json_encode(['error' => 'Account not found']);
    exit;
}

// Update and persist safely
$accounts[$user_id]['balance'] = $balance;
file_put_contents($accountsFile, json_encode($accounts, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);

echo json_encode(['status' => 'success']);

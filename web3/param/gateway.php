<?php
session_start();

// Authenticate user session
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// Validate and sanitize POST parameters
$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
$recipient = filter_input(INPUT_POST, 'recipient', FILTER_SANITIZE_STRING);

if ($amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

// Define allowlist of recipients
$allowedRecipients = ['alice', 'bob', 'charlie'];
if (!in_array($recipient, $allowedRecipients, true)) {
    http_response_code(403);
    echo json_encode(['error' => 'Recipient not allowed']);
    exit;
}

// Proceed with fund transfer logic
$userId = $_SESSION['user_id'];

// Example: call internal service or database with parameterized query
// ...

echo json_encode(['status' => 'success']);

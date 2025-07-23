<?php
session_start();
header('Content-Type: application/json');

// Ensure user is logged in
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

$userId = intval($_SESSION['user_id']);
$allowedFields = ['email', 'phone', 'address'];

// Parse and validate incoming data
$input = json_decode(file_get_contents('php://input'), true);
if (json_last_error() !== JSON_ERROR_NONE) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

$updates = [];
foreach ($input as $field => $value) {
    if (in_array($field, $allowedFields, true)) {
        $updates[$field] = htmlspecialchars(trim($value), ENT_QUOTES, 'UTF-8');
    }
}

if (empty($updates)) {
    http_response_code(400);
    echo json_encode(['error' => 'No valid fields to update']);
    exit;
}

// File path based on server-side session only
$accountFile = __DIR__ . "/accounts/{$userId}.json";
if (!file_exists($accountFile)) {
    http_response_code(404);
    echo json_encode(['error' => 'Account not found']);
    exit;
}

$data = json_decode(file_get_contents($accountFile), true);
foreach ($updates as $k => $v) {
    $data[$k] = $v;
}
file_put_contents($accountFile, json_encode($data, JSON_PRETTY_PRINT));

echo json_encode(['success' => true, 'updated' => $updates]);
<?php
session_start();
// Simple auth check, e.g., user logged in
if (!isset($_SESSION['user'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$dataFile = __DIR__ . '/data.json';
$json = json_decode(file_get_contents($dataFile), true);

// Validate and whitelist allowed fields
$allowedKeys = ['item', 'quantity', 'price'];
$update = [];
foreach ($_POST as $key => $value) {
    if (!in_array($key, $allowedKeys, true)) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid parameter: ' . $key]);
        exit;
    }
    // Basic sanitization
    $update[$key] = filter_var($value, FILTER_SANITIZE_STRING);
}

// Apply updates
$json = array_merge($json, $update);
file_put_contents($dataFile, json_encode($json, JSON_PRETTY_PRINT));

echo json_encode(['status' => 'success', 'data' => $json]);
?>
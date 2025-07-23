<?php
header('Content-Type: application/json');

// Sanitize and validate 'account' parameter
$account = filter_input(INPUT_POST, 'account', FILTER_SANITIZE_STRING);
if (!$account || !preg_match('/^[a-zA-Z0-9_]{3,30}$/', $account)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid account format']);
    exit;
}

// Define a fixed data directory and file
$dataDir = __DIR__ . '/data';
$dataFile = $dataDir . '/accounts.txt';

// Ensure directory exists with strict permissions
if (!is_dir($dataDir)) {
    mkdir($dataDir, 0700, true);
}

// Append timestamped entry with exclusive lock
$entry = date('c') . " - {$account}" . PHP_EOL;
file_put_contents($dataFile, $entry, FILE_APPEND | LOCK_EX);

echo json_encode(['status' => 'success']);
?>
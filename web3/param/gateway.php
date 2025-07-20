<?php
// gateway.php

// Require JWT library via Composer autoload
require 'vendor/autoload.php';
use \Firebase\JWT\JWT;

// Configuration
$jwtSecret = getenv('JWT_SECRET');
if (!$jwtSecret) {
    throw new Exception('JWT_SECRET must be set in environment');
}

// Read and verify Authorization header
$headers = getallheaders();
if (empty($headers['Authorization'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Missing Authorization header']);
    exit;
}
list($bearer, $token) = explode(' ', $headers['Authorization'], 2);
if (strtolower($bearer) !== 'bearer' || !$token) {
    http_response_code(401);
    echo json_encode(['error' => 'Invalid Authorization header']);
    exit;
}

try {
    $payload = JWT::decode($token, $jwtSecret, ['HS256']);
} catch (Exception $e) {
    http_response_code(401);
    echo json_encode(['error' => 'Invalid token']);
    exit;
}
$user = $payload->sub; // username or user ID

// Parse JSON input
$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['recipient'], $input['amount'])) {
    http_response_code(400);
    echo json_encode(['error' => 'recipient and amount required']);
    exit;
}
$recipient = filter_var($input['recipient'], FILTER_SANITIZE_STRING);
$amount = filter_var($input['amount'], FILTER_VALIDATE_FLOAT);
if ($amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}

// Database connection using PDO and parameters
$db = new PDO('mysql:host='.getenv('DB_HOST').';dbname='.getenv('DB_NAME'), getenv('DB_USER'), getenv('DB_PASS'), [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
]);

// Perform transfer in a transaction
try {
    $db->beginTransaction();
    // Deduct from sender
    $stmt1 = $db->prepare('UPDATE accounts SET balance = balance - ? WHERE owner = ? AND balance >= ?');
    $stmt1->execute([$amount, $user, $amount]);
    if ($stmt1->rowCount() === 0) {
        throw new Exception('Insufficient funds or invalid owner');
    }
    // Credit recipient
    $stmt2 = $db->prepare('UPDATE accounts SET balance = balance + ? WHERE owner = ?');
    $stmt2->execute([$amount, $recipient]);
    if ($stmt2->rowCount() === 0) {
        throw new Exception('Recipient account not found');
    }
    $db->commit();
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    $db->rollBack();
    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
}

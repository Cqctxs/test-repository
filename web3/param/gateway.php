<?php
session_start();
require 'config.php';  // contains DB credentials

// Ensure user is authenticated and authorized to modify balance
if (!isset($_SESSION['user_id']) || !$_SESSION['is_admin']) {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden']);
    exit;
}

// Sanitize and validate inputs
$id = filter_input(INPUT_POST, 'id', FILTER_VALIDATE_INT);
$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
if ($id === false || $amount === false) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

try {
    $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
    // Prepared statement to avoid injection
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE id = :id');
    $stmt->execute([':amt' => $amount, ':id' => $id]);
    echo json_encode(['status' => 'success']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Server error']);
}

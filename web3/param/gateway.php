<?php
// gateway.php
session_start();
require 'db_connect.php'; // Assumes PDO connection in $pdo

// Authentication check
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error'=>'Unauthorized']);
    exit;
}

// Input validation
$from_account = filter_input(INPUT_POST, 'from', FILTER_VALIDATE_INT);
$to_account   = filter_input(INPUT_POST, 'to', FILTER_VALIDATE_INT);
$amount       = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);

if ($from_account === false || $to_account === false || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid parameters']);
    exit;
}

// Authorization: ensure user owns the from_account
$stmt = $pdo->prepare('SELECT user_id, balance FROM accounts WHERE id = ?');
$stmt->execute([$from_account]);
$account = $stmt->fetch(PDO::FETCH_ASSOC);
if (!$account || $account['user_id'] != $_SESSION['user_id']) {
    http_response_code(403);
    echo json_encode(['error'=>'Forbidden']);
    exit;
}

// Check sufficient funds
if ($account['balance'] < $amount) {
    http_response_code(400);
    echo json_encode(['error'=>'Insufficient funds']);
    exit;
}

try {
    $pdo->beginTransaction();
    // Debit
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?');
    $stmt->execute([$amount, $from_account]);
    // Credit
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?');
    $stmt->execute([$amount, $to_account]);
    $pdo->commit();
    echo json_encode(['status'=>'success']);
} catch (Exception $e) {
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error'=>'Transfer failed']);
}
?>
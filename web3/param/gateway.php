<?php
// web3/param/gateway.php
session_start();
require_once 'auth.php'; // implement token-based auth

// Authenticate request
if (!validate_token($_SERVER['HTTP_AUTHORIZATION'] ?? '')) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

def sanitize_amount($amt) {
    if (!is_numeric($amt) || $amt <= 0) {
        return false;
    }
    return floatval($amt);
}

$from = filter_input(INPUT_POST, 'from', FILTER_SANITIZE_STRING);
$to = filter_input(INPUT_POST, 'to', FILTER_SANITIZE_STRING);
$amount = sanitize_amount($_POST['amount'] ?? '');

if (!$from || !$to || $amount === false) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

// Perform the balance update using a secure database API
try {
    $pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass', [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    // Begin transaction
    $pdo->beginTransaction();
    // Deduct from sender
    $stmt1 = $pdo->prepare('UPDATE accounts SET balance = balance - :amt WHERE username = :usr');
    $stmt1->execute([':amt'=>$amount,':usr'=>$from]);
    // Add to recipient
    $stmt2 = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE username = :usr');
    $stmt2->execute([':amt'=>$amount,':usr'=>$to]);
    $pdo->commit();
    echo json_encode(['message' => 'Success']);
} catch (Exception $e) {
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error'=>'Transfer failed']);
}
?>
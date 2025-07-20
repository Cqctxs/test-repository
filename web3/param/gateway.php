<?php
session_start();
// Check if user is authenticated
if (!isset($_SESSION['user_id'])) {
    header('HTTP/1.1 401 Unauthorized');
    echo json_encode(['error'=>'Authentication required']);
    exit;
}

// Validate input data
$data = json_decode(file_get_contents('php://input'), true);
if (!isset($data['account_id']) || !isset($data['amount']) || !is_numeric($data['amount'])) {
    header('HTTP/1.1 400 Bad Request');
    echo json_encode(['error'=>'Invalid input']);
    exit;
}
$account_id = intval($data['account_id']);
$amount = floatval($data['amount']);

// Authorization: ensure the session user owns the account
if ($_SESSION['user_id'] !== get_account_owner($account_id)) {
    header('HTTP/1.1 403 Forbidden');
    echo json_encode(['error'=>'Access denied']);
    exit;
}

// Proceed with balance update using prepared statements
$db = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass');
$stmt = $db->prepare('UPDATE accounts SET balance = balance + :amount WHERE id = :id');
$stmt->execute([':amount'=>$amount, ':id'=>$account_id]);

echo json_encode(['status'=>'success']);

function get_account_owner($account_id) {
    global $db;
    $stmt = $db->prepare('SELECT user_id FROM accounts WHERE id = :id');
    $stmt->execute([':id'=>$account_id]);
    return $stmt->fetchColumn();
}
?>
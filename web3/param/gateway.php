<?php
// gateway.php - fixed
// Validate and sanitize POST parameters
$account = filter_input(INPUT_POST, 'account', FILTER_SANITIZE_STRING);
$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
if ($amount === false) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid amount']);
    exit;
}
// Enforce business rules
session_start();
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error'=>'Authentication required']);
    exit;
}
$user_id = $_SESSION['user_id'];
// Use prepared statement to update balance
try {
    $pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass', [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
    $stmt = $pdo->prepare('UPDATE balances SET amount = amount + :amount WHERE account = :account AND user_id = :user_id');
    $stmt->execute([':amount'=>$amount, ':account'=>$account, ':user_id'=>$user_id]);
    echo json_encode(['message'=>'Account updated']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error'=>'Server error']);
}
?>
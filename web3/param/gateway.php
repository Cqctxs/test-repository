<?php
session_start();
// Ensure user is authenticated
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}

// Input validation
$recipient = filter_input(INPUT_POST, 'recipient', FILTER_VALIDATE_INT);
$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
if ($recipient === false || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input']);
    exit;
}

try {
    $pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass', [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
    // Verify sender balance
    $stmt = $pdo->prepare('SELECT balance FROM accounts WHERE user_id = :uid');
    $stmt->execute([':uid' => $_SESSION['user_id']]);
    $sender = $stmt->fetch(PDO::FETCH_ASSOC);
    if (!$sender || $sender['balance'] < $amount) {
        http_response_code(400);
        echo json_encode(['error' => 'Insufficient funds']);
        exit;
    }
    // Perform transfer in transaction
    $pdo->beginTransaction();
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance - :amt WHERE user_id = :uid');
    $stmt->execute([':amt' => $amount, ':uid' => $_SESSION['user_id']]);
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE user_id = :rec');
    $stmt->execute([':amt' => $amount, ':rec' => $recipient]);
    $pdo->commit();
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    if ($pdo->inTransaction()) $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error' => 'Server error']);
}
?>
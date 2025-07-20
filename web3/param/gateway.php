<?php
// web3/param/gateway.php
session_start();
// Example session-based auth: require user to be logged in
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Authentication required']);
    exit;
}
// Database connection using PDO with exceptions
db_user = 'dbuser';
db_pass = 'dbpass';
try {
    $pdo = new PDO('mysql:host=localhost;dbname=bank', db_user, db_pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Input validation
$from = filter_input(INPUT_POST, 'from', FILTER_VALIDATE_INT);
$to   = filter_input(INPUT_POST, 'to', FILTER_VALIDATE_INT);
$amt  = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
if ($from === false || $to === false || $amt === false || $amt <= 0) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid parameters']);
    exit;
}

$pdo->beginTransaction();
try {
    // check balances
    $stmt = $pdo->prepare('SELECT balance FROM accounts WHERE id = ? FOR UPDATE');
    $stmt->execute([$from]);
    $bal = $stmt->fetchColumn();
    if ($bal === false || $bal < $amt) {
        throw new Exception('Insufficient funds');
    }

    // debit
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?');
    $stmt->execute([$amt, $from]);
    // credit
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?');
    $stmt->execute([$amt, $to]);

    $pdo->commit();
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    $pdo->rollBack();
    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
}
?>
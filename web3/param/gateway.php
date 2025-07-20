<?php
session_start();
header('Content-Type: application/json');

// 1. Check for an authenticated user
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(["error" => "Unauthorized"]);
    exit;
}

// 2. Validate and sanitize input parameters
if (!isset($_POST['account_id'], $_POST['amount']) || !ctype_digit($_POST['account_id']) || !is_numeric($_POST['amount'])) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid parameters"]);
    exit;
}

$accountId = intval($_POST['account_id']);
$amount = floatval($_POST['amount']);

try {
    $pdo = new PDO(
        'mysql:host=localhost;dbname=bank',
        'username',
        'password',
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );

    // 3. Use a prepared statement and enforce user ownership
    $stmt = $pdo->prepare(
        'UPDATE accounts SET balance = balance + :amount
         WHERE id = :id AND user_id = :user_id'
    );

    $stmt->execute([
        ':amount'    => $amount,
        ':id'        => $accountId,
        ':user_id'   => $_SESSION['user_id']
    ]);

    echo json_encode(["success" => true]);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["error" => "Database error"]);
}
?>
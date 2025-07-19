<?php
// web3/param/gateway.php - Secure version with validation and authorization
session_start();
require 'auth.php'; // handles session and user roles

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF token check
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
        http_response_code(403);
        exit('Invalid CSRF token');
    }

    // Validate inputs
    $userId = filter_input(INPUT_POST, 'user_id', FILTER_VALIDATE_INT);
    $amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_FLOAT);
    $action = $_POST['action'] ?? '';

    if ($userId === false || $amount === false || $amount <= 0) {
        http_response_code(400);
        exit('Invalid parameters');
    }

    // Authorization: only admins can credit/debit balance
    if (!is_admin($_SESSION['user_role'])) {
        http_response_code(403);
        exit('Insufficient privileges');
    }

    // Prevent directory traversal
    $filename = basename($_POST['filename'] ?? '');
    if (empty($filename)) {
        http_response_code(400);
        exit('Missing filename');
    }

    // Perform balance update safely using parameterized queries
    $pdo = new PDO('mysql:host=localhost;dbname=bank', 'user', 'pass', [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
    if ($action === 'credit') {
        $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE user_id = :uid');
    } else if ($action === 'debit') {
        $stmt = $pdo->prepare('UPDATE accounts SET balance = balance - :amt WHERE user_id = :uid');
    } else {
        http_response_code(400);
        exit('Invalid action');
    }
    $stmt->execute([':amt'=>$amount, ':uid'=>$userId]);

    // File write example: only to uploads directory
    $target = __DIR__ . '/uploads/' . $filename;
    file_put_contents($target, $_POST['data'] ?? '');

    echo 'Success';
}
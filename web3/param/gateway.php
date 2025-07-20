<?php
session_start();
header('Content-Type: application/json');

// Use PDO with prepared statements for DB operations
$dsn = getenv('DB_DSN');
$user = getenv('DB_USER');
$pass = getenv('DB_PASS');
$options = [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION];
$pdo = new PDO($dsn, $user, $pass, $options);

// Simple authentication check (e.g., after login)
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}
$user_id = (int) $_SESSION['user_id'];

// Parse JSON input
$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['error' => 'Bad Request']);
    exit;
}

$action = $input['action'] ?? '';
$account_id = isset($input['id']) ? (int)$input['id'] : null;
$amount = isset($input['amount']) ? (float)$input['amount'] : null;

switch ($action) {
    case 'deposit':
        $stmt = $pdo->prepare(
            'UPDATE accounts SET balance = balance + :amt WHERE id = :id AND user_id = :uid'
        );
        $stmt->execute([':amt' => $amount, ':id' => $account_id, ':uid' => $user_id]);
        break;

    case 'withdraw':
        // Verify balance
        $stmt = $pdo->prepare(
            'SELECT balance FROM accounts WHERE id = :id AND user_id = :uid'
        );
        $stmt->execute([':id' => $account_id, ':uid' => $user_id]);
        $balance = $stmt->fetchColumn();
        if ($balance === false || $balance < $amount) {
            http_response_code(400);
            echo json_encode(['error' => 'Insufficient funds']);
            exit;
        }
        $stmt = $pdo->prepare(
            'UPDATE accounts SET balance = balance - :amt WHERE id = :id AND user_id = :uid'
        );
        $stmt->execute([':amt' => $amount, ':id' => $account_id, ':uid' => $user_id]);
        break;

    default:
        http_response_code(400);
        echo json_encode(['error' => 'Invalid action']);
        exit;
}

echo json_encode(['success' => true]);
?>
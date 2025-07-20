<?php
// Input validation and simple auth token check
function validate_amount($amt) {
    if (!is_numeric($amt) || $amt < 0) {
        throw new Exception('Invalid amount');
    }
    return (float) $amt;
}

function authenticate() {
    $headers = getallheaders();
    if (empty($headers['Authorization'])) {
        http_response_code(401);
        exit('Unauthorized');
    }
    // Validate token format here...
}

authenticate();

try {
    $account = $_POST['account'] ?? '';
    $amount = validate_amount($_POST['amount'] ?? 0);

    // Proceed with account manipulation safely
    // e.g., prepared statements
    $pdo = new PDO('mysql:host=localhost;dbname=mydb', 'user', 'pass');
    $stmt = $pdo->prepare('UPDATE accounts SET balance = balance + :amt WHERE account = :acct');
    $stmt->execute([':amt' => $amount, ':acct' => $account]);
    echo json_encode(['status' => 'success']);
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
}
?>
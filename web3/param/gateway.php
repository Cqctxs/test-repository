<?php
// gateway.php - secure transfer endpoint
// Require an API token in Authorization header
$headers = getallheaders();
if (!isset($headers['Authorization'])) {
    http_response_code(401);
    exit('Unauthorized');
}
$token = str_replace('Bearer ', '', $headers['Authorization']);
if ($token !== getenv('API_TOKEN')) {
    http_response_code(403);
    exit('Forbidden');
}

// Validate POST parameters
if (!isset($_POST['from'], $_POST['to'], $_POST['amount'])) {
    http_response_code(400);
    exit('Missing parameters');
}
if (!preg_match('/^\d+$/', $_POST['from']) || !preg_match('/^\d+$/', $_POST['to'])) {
    http_response_code(400);
    exit('Invalid account format');
}
if (!is_numeric($_POST['amount'])) {
    http_response_code(400);
    exit('Invalid amount');
}
$amount = floatval($_POST['amount']);
if ($amount <= 0) {
    http_response_code(400);
    exit('Amount must be positive');
}

// Load and lock accounts file
$file = __DIR__ . '/accounts.json';
$fp = fopen($file, 'c+');
if (flock($fp, LOCK_EX)) {
    $data = stream_get_contents($fp);
    $accounts = json_decode($data, true) ?? [];

    if (!isset($accounts[$_POST['from']], $accounts[$_POST['to']])) {
        http_response_code(404);
        flock($fp, LOCK_UN);
        exit('Account not found');
    }
    if ($accounts[$_POST['from']] < $amount) {
        http_response_code(400);
        flock($fp, LOCK_UN);
        exit('Insufficient funds');
    }
    $accounts[$_POST['from']] -= $amount;
    $accounts[$_POST['to']] += $amount;
    
    // Write back with truncation
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($accounts, JSON_PRETTY_PRINT));
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);

    echo 'Transfer successful';
} else {
    fclose($fp);
    http_response_code(500);
    exit('Could not lock file');
}
?>
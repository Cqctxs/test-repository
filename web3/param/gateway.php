<?php
session_start();
// Simple authentication stub
if (!isset($_SESSION['user']) || $_SESSION['role'] !== 'admin') {
    http_response_code(401);
    echo json_encode(['error'=>'Unauthorized']);
    exit;
}
$data = json_decode(file_get_contents('php://input'), true);
$from = filter_var($data['from'], FILTER_SANITIZE_STRING);
$to = filter_var($data['to'], FILTER_SANITIZE_STRING);
$amount = filter_var($data['amount'], FILTER_VALIDATE_FLOAT);
if ($from === false || $to === false || $amount === false || $amount <= 0) {
    http_response_code(400);
    echo json_encode(['error'=>'Invalid parameters']);
    exit;
}
$ledgerFile = __DIR__ . '/ledger.json';
$ledger = json_decode(file_get_contents($ledgerFile), true);
if (!isset($ledger[$from]) || !isset($ledger[$to])) {
    http_response_code(404);
    echo json_encode(['error'=>'Account not found']);
    exit;
}
if ($ledger[$from] < $amount) {
    http_response_code(400);
    echo json_encode(['error'=>'Insufficient funds']);
    exit;
}
// Perform transfer
$ledger[$from] -= $amount;
$ledger[$to] += $amount;
// Write back atomically
tmpFile = $ledgerFile . '.tmp';
file_put_contents($tmpFile, json_encode($ledger, JSON_PRETTY_PRINT));
rename($tmpFile, $ledgerFile);

echo json_encode(['status'=>'success','from'=>$from,'to'=>$to,'amount'=>$amount]);
?>
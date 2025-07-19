<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $json = file_get_contents('accounts.json');
    $json_data = json_decode($json,true);

    $json_data[$_POST['recipient']] += $_POST['amount'];
    $json_data[$_POST['sender']] -= $_POST['amount'];
    
    file_put_contents('accounts.json', json_encode($json_data));
}

if ($_SERVER["REQUEST_METHOD"] === "GET") {
    echo file_get_contents('accounts.json');
}
?>
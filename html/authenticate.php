<?php
session_start();
if(isset($_COOKIE["keepme"])) {
    $result = file_get_contents('http://127.0.0.1/mydomus/api/checktoken/'.$_COOKIE["keepme"]);
    $result_json = json_decode($result, true);
    if($result_json['status'] == 'ok') {
            $_SESSION['authenticated'] = 'true';
            $_SESSION['token'] = $_COOKIE["keepme"];
    }
}
if(empty($_SESSION["authenticated"]) || $_SESSION["authenticated"] != 'true') {
    header('Location: login.php', true, 302);
    exit;
}
?>
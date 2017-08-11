<?php
require_once('authenticate.php');
$string = file_get_contents("mydomus.conf");
$conf= json_decode($string, true);
$result = file_get_contents('http://127.0.0.1:'.strval($conf['ServerPort']).$_POST['url']);
echo $result;
?>
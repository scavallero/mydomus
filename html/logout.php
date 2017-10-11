<?php
session_start();
session_destroy(); 
if(isset($_COOKIE["keepme"])) {
    setcookie ("keepme","");
}
header("Location: index.php", true, 302);
exit;
?>


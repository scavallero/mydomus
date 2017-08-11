<?php
session_start();
session_destroy(); 
header("Location: index.php", true, 302);
exit;
?>


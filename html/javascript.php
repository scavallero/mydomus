<?php 
	require_once('authenticate.php');
	header("Content-type: application/javascript"); 
?>

mydomusToken = <?php echo '"'.$_SESSION['token'].'"'; ?>;

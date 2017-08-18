<?php
session_start();
$email = null;
$password = null;
$adminemail = 'user@gmail.com';
$adminpassword = 'password';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if(!empty($_POST["email"]) && !empty($_POST["password"])) {
        $email = $_POST["email"];
        $password = $_POST["password"];     
        if($email == $adminemail && $password == $adminpassword) {
            $_SESSION["authenticated"] = 'true';
            header("Location: index.php", true, 302);
            exit;
        }
        else {
            header('Location: login.php', true, 302);
            exit;
        }
    } else {
        header('Location: login.php', true, 302);
        exit;
    }
} else if(!empty($_SESSION["authenticated"])) {
    header('Location: index.php', true, 302);
    exit;
} else {
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>MyDomus Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="css/mydomus.css" />
		<link rel="stylesheet" href="css/jquery.mobile.icons.min.css" />
		<link rel="stylesheet" href="css/jquery.mobile.structure-1.4.5.min.css" />
		<script src="js/jquery-1.11.1.min.js"></script>
		<script src="js/jquery.mobile-1.4.5.min.js"></script>
        <!--
		<script src="js/highcharts.js"></script>
		<script src="js/highcharts-more.js"></script>
		<script src="js/main.js"></script>
        <script src="js/trial.js"></script>
        -->
    </head>
    <body> 
	
	<div data-role="page">
		<center>
            <div id="main" role="main" class="ui-content" style="width:300px">
               
			   	<div class="ui-body">
					<h2>Please sign in </h2>
				</div>

				<ul data-role="listview" data-inset="true">
                    <li>
						<!-- <form class="form-signin" action="login.php" method="POST"> -->
                        <form class="form-signin" action="login.php" method="POST" data-ajax="false">
							<div class="ui-body ui-corner-all">
								<label for="inputEmail">Email address</label>
								<input type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus name="email">
								<label for="inputPassword">Password</label>
								<input type="password" id="inputPassword" class="form-control" placeholder="Password" required name="password">
								<div class="checkbox">
									<label>
										<input type="checkbox" value="remember-me" name="remember"> <p>Remember me</p>
									</label>
								</div>
							</div>
						<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
						</form>
                    </li>
                </ul>
			</div>
		</center>
    </div>
    
</body>

</html>

<?php } ?>
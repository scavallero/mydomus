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
<html>
<head>
    <title>WebApp</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/main.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <script src="js/jquery-3.1.1.min.js"></script>
    <script src="js/bootstrap.min.js"></script> 
    <script src="js/main.js"></script>
</head>

<body>    
    <!-- Navbar -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<div class="container-fluid">
			<div class="navbar-header">
    			<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        			<span class="sr-only">Toggle navigation</span>
        			<span class="icon-bar"></span>
        			<span class="icon-bar"></span>
        			<span class="icon-bar"></span>
    			</button>
                <div  class="navbar-brand">MyDomus</div>
			</div>
			<div id="navbar" class="collapse navbar-collapse">
				<ul class="nav navbar-nav">
					<li class="acrive"><a href="index.php"><span class="fa fa-home solo">Home</span></a></li>
					<li><a href="#anch1"><span class="fa fa-anchor solo">Alerts</span></a></li>
				</ul>
				<ul class="nav navbar-nav navbar-right">
					<li><a href="logout.php"><span class="glyphicon glyphicon-log-out"></span> Sign Out</span></a></li>
				</ul>
			</div>
		</div>
	</nav>
	
    <div class="container">

        <form class="form-signin" action="login.php" method="POST">
            <h2 class="form-signin-heading">Please sign in </h2>
            <label for="inputEmail" class="sr-only">Email address</label>
            <input type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus name="email">
            <label for="inputPassword" class="sr-only">Password</label>
            <input type="password" id="inputPassword" class="form-control" placeholder="Password" required name="password">
            <div class="checkbox">
            <label>
                <input type="checkbox" value="remember-me" name="remember"> <p>Remember me</p>
            </label>
            </div>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
        </form>

    </div> <!-- /container -->
</body>
</html>
<?php } ?>
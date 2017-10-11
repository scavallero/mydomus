<?php
session_start();
$user = null;
$password = null;

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if(!empty($_POST["user"]) && !empty($_POST["password"])) {
        $user = $_POST["user"];
        $password = md5($_POST["password"]);    
        $string = file_get_contents("mydomus.conf");
        $conf = json_decode($string, true);
        $result = file_get_contents('http://127.0.0.1:'.strval($conf['ServerPort']).'/verify/'.$user.'/'.$password);
        $result_json = json_decode($result, true);
        if($result_json['status'] == 'ok') {
            $_SESSION['authenticated'] = 'true';
            $_SESSION['token'] = $result_json['token'];
            
            // Remember me cookie
            if (!empty($_POST["remember"])) {
                setcookie ("keepme",$result_json['token'],time()+ (10 * 365 * 24 * 60 * 60));
            }
            
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

			</div>
		</div>
	</nav>
	
    <div class="container">

        <form class="form-signin" action="login.php" method="POST">
            <h2 class="form-signin-heading">Please sign in </h2>
            <label for="inputUser" class="sr-only">User</label>
            <input type="text" id="inputUser" class="form-control" placeholder="User" required autofocus name="user">
            <label for="inputPassword" class="sr-only">Password</label>
            <input type="password" id="inputPassword" class="form-control" placeholder="Password" required name="password">
            <div class="checkbox">
            <label>
                <input type="checkbox" value="true" name="remember"> <p>Keep me signed in</p>
            </label>
            </div>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
        </form>

    </div> <!-- /container -->
</body>
</html>
<?php } ?>
<?php
require_once('authenticate.php');
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
    <script src="js/highcharts.js"></script>
	<script src="js/highcharts-more.js"></script>
    <script src="js/modules/exporting.js"></script>
	<script src="js/chart-style.js"></script>
	<script src="js/main.js"></script>
</head>

<body onload="doDashboard();">    
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

    <!-- Page content -->
    <div class="page-content">
        <div class="container-fluid">
            <div id="sensorlist"></div>
        </div>
    </div>

</body>
</html>
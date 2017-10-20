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
    <script src="js/bootstrap-table.min.js"></script>
    <script src="js/highcharts.js"></script>
	<script src="js/highcharts-more.js"></script>
    <script src="js/modules/exporting.js"></script>
	<script src="js/chart-style.js"></script>
	<script src='javascript.php'></script>
	<script src="js/main.js"></script>
	
</head>
<body onload="doSettings();">
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
				<ul class="nav navbar-nav navbar-right">
					<li><a href="settings.php"><span class="glyphicon glyphicon-cog"></span> Settings</span></a></li>
				</ul>
			</div>
		</div>
	</nav>

    <!-- Page content -->

	<div class="container-fluid">
		<div class="row">
			<div class="col-sm-12 col">
		
				<div id="settings_data">
				</div>
				
				<form class="input-append">
					<div id="field">
						<label for="field_token">User token:</label>
						<input autocomplete="off" class="input" id="field_token" name="prof1" type="text" size="60" readonly></input>
					</div>
				</form>
                <br>
                <h2> Metrics Manager </h3>
                <table id="metrics_table">
                    <thead>
                        <tr>
                            <th data-field="ChkboxEnabled" data-align="center" >Enabled</th>
                            <th data-field="Metric" data-align="center">Metric</th>
                            <th data-field="Sensor" data-align="center">Sensor</th>
                            <th data-field="MClass" data-align="center">Class</th>
                            <th data-field="Filename" data-align="center">Config Filename</th>
                            <th data-field="BtnReset" data-align="center">Action</th>
                        </tr>
                    </thead>
                </table>

			</div>
		</div>
		<div>
			<a href="index.php" class="btn btn-success">Apply</a> <a href="index.php" class="btn btn-primary">Cancel</a>
		</div>
        <br>
        <h2> System Errors </h3>
        <div>
            <textarea class="form-control" rows="10" id="logs" readonly></textarea>
        </div>
	</div>

	
</body>
</html>

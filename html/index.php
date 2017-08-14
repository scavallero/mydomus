<?php
require_once('authenticate.php');
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>MyDomus</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="css/mydomus.css" />
		<link rel="stylesheet" href="css/jquery.mobile.icons.min.css" />
		<link rel="stylesheet" href="css/jquery.mobile.structure-1.4.5.min.css" />
		<script src="js/jquery-1.11.1.min.js"></script>
		<script src="js/jquery.mobile-1.4.5.min.js"></script>
		<script src="js/highcharts.js"></script>
		<script src="js/highcharts-more.js"></script>
        <script src="js/modules/exporting.js"></script>
		<script src="js/main.js"></script>
        <script src="js/trial.js"></script>
    </head>
    <body>
        <div data-role="page">
            <div id="panel-menu" data-role="panel" data-display="overlay">
                <a href="index.php" class="ui-btn" data-ajax="false">Dashboard</a>
                <a href="#" url="./PageOne.html" class="ui-btn">Page One</a>
                <a href="logout.php" class="ui-btn" data-ajax="false">Sign Out</a>
            </div>
            <div data-role="header" data-position="fixed">
                <h1>MyDomus</h1>
                <a href="#panel-menu" class="ui-btn ui-corner-all ui-icon-bars ui-btn-icon-notext">Menu</a>
            </div>
            <div id="main" role="main" class="ui-content">
                <div data-role="collapsible-set"  id="sensorlist">
                </div>
            </div>
        </div>
        <script>
        doAll();
        console.log("Eseguito !!");
        </script>
    </body>
</html>

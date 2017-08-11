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
                <a href="#" url="./Home.html" class="ui-btn">Home</a>
                <a href="#" url="./PageOne.html" class="ui-btn">Page One</a>
                <a href="logout.php" class="ui-btn">Sign Out</a>
            </div>
            <div data-role="header" data-position="fixed">
                <h1>MyDomus</h1>
                <a href="#panel-menu" class="ui-btn ui-corner-all ui-icon-bars ui-btn-icon-notext">Menu</a>
            </div>
            <div id="main" role="main" class="ui-content">
                <div data-role="collapsible-set"  id="sensorlist">
                </div>
                <!--
				<div data-role="collapsible">
                    <h4>Sensor 1</h4>
                    <div class="ui-grid-a ui-responsive">
                        <div class="ui-block-a">
                            <div id="gauge_temp">
                            </div>
                        </div>
                        <div class="ui-block-b">
                            <div id="graph_temp">
                            </div>
                        </div>
                    </div>
				</div>
				<div data-role="collapsible">
                    <h4>Sensor 2</h4>
                    <div class="ui-grid-a ui-responsive">
                        <div class="ui-block-a">
                            <div id="gauge_temp_2">
                            </div>
                        </div>
                        <div class="ui-block-b">
                            <div id="graph_temp_2">
                            </div>
                        </div>
                    </div>
				</div>
				<div data-role="collapsible">
                    <h4>Sensor 3</h4>
                    <div class="ui-grid-a ui-responsive">
                        <div class="ui-block-a">
                            <div id="gauge_temp_3">
                            </div>
                        </div>
                        <div class="ui-block-b">
                            <div id="graph_temp_3">
                            </div>
                        </div>
                    </div>
				</div>
                -->
            </div>
        </div>
        <script>
        doAll();
        console.log("Eseguito !!");
        </script>
    </body>
</html>

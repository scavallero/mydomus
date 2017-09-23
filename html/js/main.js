function CreateDynamicGauge(sensorname,val) {
	
	$.post("gateway.php",{"url": "/get/sensor/"+sensorname},function(response){
		var newVal = JSON.parse(response);
		style = gauge_style;
		//style = linear_gauge_style;
		style.title.text = newVal.ylabel
		
		if (newVal.unit != "") {
			style.yAxis.title.text = newVal.unit;
		} else {
			style.yAxis.title.text = "";
		}
		style.series = [{
			name: 'Current Value',
			data: [newVal.value],
			tooltip: {
				valueSuffix: "  "+newVal.unit
			}
		}];
		
		var chart1 = Highcharts.chart('gauge_'+sensorname,style,function (chart) {
			if (!chart.renderer.forExport) {
				setInterval(function () {
					if(chart.series) { // Prevent calls on false redraw
						var point = chart.series[0].points[0];
						$.post("gateway.php",{"url": "/get/sensor/"+sensorname},function(response){
						var newVal = JSON.parse(response);
						point.update(newVal.value); 
						});
					}
				}, 30000);
			}
		});
	});          
}
	

function CreateDynamicGraph(sensorname,val) {
	$.post("gateway.php",{"url": "/get/daily/"+sensorname},function(response){
	var newVal = JSON.parse(response);
	var data = newVal.value;      
	var style = graph_style;
	style.title.text = sensorname+' last 24 hours data';

	style.yAxis.title.text = newVal.ylabel;
	if (newVal.unit != "") {
		style.yAxis.title.text = newVal.ylabel+"  ["+newVal.unit+"]";
	}
	style.series = [{
		type: 'area',
		name: 'Temp',
		data: data
	}];

	var graph1 = Highcharts.chart('graph_'+sensorname,style,function (chart) {
		if (!chart.renderer.forExport) {
			setInterval(function () {
				if(chart.series) { // Prevent calls on false redraw
					$.post("gateway.php",{"url": "/get/daily/"+sensorname},function(response){
						var newVal = JSON.parse(response);
						var data = newVal.value; 
						chart.series[0].update({
							type: 'area',
							name: 'Temp',
							data: data
						}, true); //true / false to redraw
					});
				}
			}, 120000);
		}
	});
	});
}

function doHistory(sensor,param) {

	console.log("Historical Data !!");
	console.log(sensor);
	console.log(param);
	$.post("gateway.php",{"url": "/get/sensor/config"},function(response){
        var jsonresp = JSON.parse(response);
        var groups = jsonresp['value'];
		jQuery.each(groups, function(item, val) {
			jQuery.each(val['Metrics'], function(sensorname, val) {
				if (sensor == sensorname) {
					$.post("gateway.php",{"url": "/get/history/"+sensorname},function(response){
						var newVal = JSON.parse(response);
						var avg = newVal.avg;
						var rng = newVal.rng;
						var style = graph_history_style;
						style.chart.backgroundColor = "#FFFFFF";
						style.title.text = sensorname+' history data';
						style.yAxis.title.text = newVal.ylabel;
						if (newVal.unit != "") {
							style.yAxis.title.text = newVal.ylabel+"  ["+newVal.unit+"]";
						}
						style.series = [{
							name: 'Average',
							data: avg,
							marker: {
								enabled: false
							}
						},{
							name: 'Range',
							data: rng,
							type: 'arearange',
							lineWidth: 0,
							linkedTo: ':previous',
							fillOpacity: 0.3,
							zIndex: 0,
							marker: {
								enabled: false
							}
						}];
						var chart1 = Highcharts.chart('hdata',style);
					});
				}
			});
		});
	});
}


function doDashboard() {
    
    $.post("gateway.php",{"url": "/get/sensor/config"},function(response){
        var jsonresp = JSON.parse(response);
        var groups = jsonresp['value'];
        var html='<div class="panel-group" id="accordion">'
        jQuery.each(groups, function(item, val) {
            jQuery.each(val['Metrics'], function(sensorname, val) {
                html +='    <div class="panel panel-default">';
                html += '        <div class="panel-heading">'
                html += '           <h4 class="panel-title">'
                html += '               <a data-toggle="collapse" data-parent="#accordion" href="#_'+sensorname+'">'+sensorname+'</a>'
                html += '           </h4>'
                html += '        </div>'
                html += '        <div id="_'+sensorname+'" class="panel-collapse collapse">'
                html += '            <div class="panel-body">'
                html += '                <div class="row">'
                html += '                    <div class="col-md-3 col-xs-12">'
                html += '                        <div class="panel panel-success">'
                html += '                            <div class="panel-heading">'
                html += '                            </div>'
                html += '                            <div class="panel-body">'
                html += '                                <div id="gauge_'+sensorname+'">';
                html += '                                </div>'                
                html += '                            </div>'
                html += '                         </div>'
                html += '                    </div>'
                html += '                    <div class="col-md-9 col-xs-12">'
                html += '                        <div class="panel panel-success">'
                html += '                            <div class="panel-heading">'
                html += '                            </div>'
				html += '                            <div class="panel-body">'
				html += '                                <div id="graph_'+sensorname+'"/>';
                html += '                            </div>'
                html += '                         </div>'
                html += '                     </div>'
                html += '                </div>'
                html += '                <br><a class="btn btn-primary btn-block" href="history.php?sensor='+sensorname+'&param=null'+'">View history</a>';                
                html += '            </div>'
                html += '        </div>'
                html +='    </div>';
            });
        });
        html +='</div>';
        $("#sensorlist").html(html);
		
		// Redraw graph on callapse shown and hide
		$(".collapse").on('shown.bs.collapse hidden.bs.collapse', function() {
			Highcharts.charts.forEach(function(chart) {
				chart.reflow();
			});
		});
  
        jQuery.each(groups, function(item, val) {   
            jQuery.each(val['Metrics'], function(sensorname, val) {            
                
                // Create dynamic gauge
				CreateDynamicGauge(sensorname,val);
				
                // Create dynamic graph
                CreateDynamicGraph(sensorname,val);
                
                console.log(sensorname);
            });
        });  
    });
}


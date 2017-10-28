function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

function mydomusApi(api,fn,method,b) {
    if (method == undefined || method == 'get') {
        $.get("api"+api+'/'+mydomusToken,fn);
    } else if (method == 'post') {
		if (b == undefined)
			$.post("api"+api+'/'+mydomusToken,fn);
		else
			$.post("api"+api+'/'+mydomusToken,b,fn)
    }
}

function callSensor(s,param) {
		mydomusApi("/call/sensor/"+s,function(jsonresp){
			console.log(jsonresp);
		},'post','{"value":'+param+'}');
}

function doSettings() {
    
    var data = [];
    
    $("#field_token").val(mydomusToken);
	
	mydomusApi("/get/config",function(jsonresp){
        var groups = jsonresp['value'];
        i = 0;
		jQuery.each(groups, function(sensorname, val) {
			jQuery.each(val['Metrics'], function(metricname, mval) {
				var btn = '<a class="btn btn-warning" href="history.php?sensor='+metricname+'&param=null'+'">View history</a>'
				btn += '&nbsp;&nbsp;<button type="button" class="btn btn-danger">Delete History <span class="glyphicon glyphicon-remove-sign"></span></button>'
				
				data[i] = {
                    "ChkboxEnabled" : '<input type="checkbox" id="ch'+i+'" checked="true"></input>',
                    "Metric" : metricname,
                    "Sensor" :sensorname,
                    "MClass"  : mval['Class'],
                    "Filename" : val['Filename'],
                    "BtnReset" : btn
                };
                i++;
			});
		});
        $('#metrics_table').bootstrapTable({
        data: data,
        striped: true,
        pagination: true,
        pageSize: 10
        });
	});
    
    $.get("api/",function(jsonresp){
        var logs = jsonresp['log'];
        var txt = ""
        for (i = 0; i < logs.length; i++) { 
            txt += logs[i] + "\n";
        }
        $('#logs').val(txt);
    }); 
    
}

function CreateDynamicGauge(sensorname,val) {
	
	//console.log(val);
	
	mydomusApi("/get/sensor/"+sensorname,function(newVal){
		style = gauge_style;
		style.title.text = newVal.ylabel;

		style.series = [{
			name: 'Current Value',
			data: [newVal.value],
			tooltip: {
				valueSuffix: "  "+newVal.unit
			}
		}];
        
		switch (val.Class) {
			case 'temp_c':
				style.yAxis= y_temperature;
			break;

			case 'cpu_temp_c':
			case 'relative_humidity':
				style.yAxis= y_0_100;
			break;
			
			case 'pressure_mb':
				style.yAxis= y_barometer;
			break;
			
			case 'power':
            case 'active_power':
				style.yAxis= y_power;
			break;
			
			default:
			style.yAxis= y_default;
		}
		
		if (newVal.unit != "") {
			style.yAxis.title.text = newVal.unit;
		} else {
			style.yAxis.title.text = "";
		}
        
        if (val.Class == 'wethermo_temp') {
            var wt = new WeThermo(sensorname);
            wt.draw(parseFloat(newVal.value));
            setInterval(function () {
                mydomusApi("/get/sensor/"+sensorname,function(newVal){
                    wt.draw(parseFloat(newVal.value));
                });
            }, 30000);
            
        } else {
            var chart1 = Highcharts.chart('gauge_'+sensorname,style,function (chart) {
                if (!chart.renderer.forExport) {
                    setInterval(function () {
                        if(chart.series) { // Prevent calls on false redraw
                            var point = chart.series[0].points[0];
                            mydomusApi("/get/sensor/"+sensorname,function(newVal){
                                point.update(newVal.value); 
                            });
                        }
                    }, 30000);
                }
            });
        }
	});          
}
	

function CreateDynamicGraph(sensorname,val) {
	mydomusApi("/get/daily/"+sensorname,function(newVal){
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
	
	if (newVal.mclass == 'energy') {
		style.series = [{
			type: 'column',
			name: 'Temp',
			data: data
		}];
	}

	var graph1 = Highcharts.chart('graph_'+sensorname,style,function (chart) {
		if (!chart.renderer.forExport) {
			setInterval(function () {
				if(chart.series) { // Prevent calls on false redraw
					mydomusApi("/get/daily/"+sensorname,function(newVal){
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
	mydomusApi("/get/config",function(jsonresp){
        var groups = jsonresp['value'];
		jQuery.each(groups, function(item, val) {
			jQuery.each(val['Metrics'], function(sensorname, val) {
				if (sensor == sensorname) {
					mydomusApi("/get/history/"+sensorname+"/"+param,function(newVal){
						var avg = newVal.avg;
						var rng = newVal.rng;
						var cnt	= [];
						
						// For energy counter plot only max values
						if (newVal.mclass == 'energy') {
							for (var i = 0; i < rng.length; i++) {
								cnt[i] = [rng[i][0],rng[i][2]]
							}
						}
						
						var style = graph_history_style;
						style.chart.backgroundColor = "#FFFFFF";
						if (param == 30) {
							style.title.text = sensorname+' last 30 days data';
						} else {
							style.title.text = sensorname+' history data';
						}
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
						
						// For energy counter plot only max values
						if (newVal.mclass == 'energy') {
							style.series = [{
								name: 'Count',
								data: cnt,
								type: 'column'
							}];
						}
						
						var chart1 = Highcharts.chart('hdata',style);
					});
				}
			});
		});
	});
}


function doDashboard() {
    
	mydomusApi("/get/config",function(jsonresp){
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
				html += '                <br><a class="btn btn-primary btn-block" href="history.php?sensor='+sensorname+'&param=30'+'">View last 30 days</a>';              
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


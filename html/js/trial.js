/**
 * Get the current time
 */
 
function doHistory(sensor,param) {
    doTheme();
    doStyle();
	console.log("Historical Data !!");
	console.log(sensor);
	console.log(param);
	jQuery.each(groups, function(item, val) {
        jQuery.each(val['Peripherials'], function(sensorname, val) {
			if sensor == sensorname {
				console.log("Sensor exists!);
		}
	}
}

function doDashboard() {

    doTheme();
    doStyle();
    
    $.post("gateway.php",{"url": "/get/sensor/config"},function(response){
        var jsonresp = JSON.parse(response);
        var groups = jsonresp['value'];
        jQuery.each(groups, function(item, val) {
            jQuery.each(val['Peripherials'], function(sensorname, val) {
                var html='';
                html += '<div data-role="collapsible">';
                html +=   '<h4>'+sensorname+'</h4>';
                html +=   '<div class="ui-grid-a ui-responsive">'
                html +=     '<div class="ui-block-a">';
                html +=       '<div id="gauge_'+sensorname+'">';
                html +=       '</div>';
                html +=     '</div>';
                html +=     '<div class="ui-block-b">';
                html +=       '<div id="graph_'+sensorname+'">';
                html +=       '</div>';
                html +=     '</div>';
                html +=   '</div>';
                html += '</div>';
                $("#sensorlist").append(html).collapsibleset('refresh');;
                
                // Create dynamic gauge
                $.post("gateway.php",{"url": "/get/sensor/"+sensorname},function(response){
                    var newVal = JSON.parse(response);
                    style = temperature_style;
                    style.series = [{
                        name: 'Current Value',
                        data: [newVal.value],
                        tooltip: {
                            valueSuffix: 'C'
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

                // Create dynamic graph
                $.post("gateway.php",{"url": "/get/daily/"+sensorname},function(response){
                    var newVal = JSON.parse(response);
                    var data = newVal.value;      
                    var style = graph_style;
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
                console.log(sensorname);
            });
        });  
    });
}

function doTheme() {
    
    Highcharts.setOptions({
        global: {
            useUTC: false
        },
        credits: {
			enabled: false
		}
    });

    Highcharts.theme = {
       colors: ['#f45b5b', '#8085e9', '#8d4654', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
          '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
       chart: {
          backgroundColor: null,
          style: {
             fontFamily: 'Signika, serif'
          }
       },
       title: {
          style: {
             color: 'black',
             fontSize: '16px',
             fontWeight: 'bold'
          }
       },
       subtitle: {
          style: {
             color: 'black'
          }
       },
       tooltip: {
          borderWidth: 0
       },
       legend: {
          itemStyle: {
             fontWeight: 'bold',
             fontSize: '13px'
          }
       },
       xAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       yAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       plotOptions: {
          series: {
             shadow: true
          },
          candlestick: {
             lineColor: '#404048'
          },
          map: {
             shadow: false
          }
       },

       // Highstock specific
       navigator: {
          xAxis: {
             gridLineColor: '#D0D0D8'
          }
       },
       rangeSelector: {
          buttonTheme: {
             fill: 'white',
             stroke: '#C0C0C8',
             'stroke-width': 1,
             states: {
                select: {
                   fill: '#D0D0D8'
                }
             }
          }
       },
       scrollbar: {
          trackBorderColor: '#C0C0C8'
       },

       // General
       background2: '#E0E0E8'

    };

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);
}

function doStyle() {
    
	temperature_style = {

        chart: {
            type: 'gauge',
			backgroundColor: $("body").css("background-color"),
            plotBorderWidth: 0,
            plotShadow: false
        },

        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },

        // the value axis
        yAxis: {
            min: 0,
            max: 120,

            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: 'C'
            },
            plotBands: [{
                from: 0,
                to: 60,
                color: '#55BF3B' // green
            }, {
                from:60,
                to: 80,
                color: '#DDDF0D' // yellow
            }, {
                from: 80,
                to: 120,
                color: '#DF5353' // red
            }]
        }
    }
	
    graph_style = {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'Daily Values'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Temperature'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        }
    }
}